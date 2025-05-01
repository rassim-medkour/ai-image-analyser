"""
Image Analysis Service: Handles interactions with AI vision APIs for image analysis.
Currently implemented with Clarifai, but designed to be extendable for other providers.
"""
import sys
import traceback
from flask import current_app

# Conditional import to handle missing dependencies gracefully
try:
    # Updated imports for Clarifai version 11.2+
    from clarifai.client.user import User
    from clarifai.client.workflow import Workflow
    CLARIFAI_AVAILABLE = True
except ImportError as e:
    current_app.logger.error(f"Clarifai import error: {str(e)}, paths: {sys.path}")
    CLARIFAI_AVAILABLE = False


class ImageAnalysisService:
    """Generic image analysis service that uses Clarifai as the default provider"""
    
    def __init__(self, provider="clarifai"):
        """
        Initialize the image analysis service.
        
        Args:
            provider (str): The AI provider to use ('clarifai' by default)
        """
        self.provider = provider
        self.pat = None
        self.is_available = False
        self.workflow_url = None
        self.user = None
        
        # Try to initialize the client based on the provider
        try:
            if provider == "clarifai":
                if not CLARIFAI_AVAILABLE:
                    current_app.logger.warning("Clarifai package is not installed. Image analysis will be disabled.")
                    return
                    
                self.pat = current_app.config.get('CLARIFAI_PAT')
                if not self.pat:
                    current_app.logger.warning("CLARIFAI_PAT is not set in the application configuration. Image analysis will be disabled.")
                    return
                
                # Get the workflow URL from configuration
                self.workflow_url = current_app.config.get('CLARIFAI_WORKFLOW_URL')
                if not self.workflow_url:
                    current_app.logger.warning("CLARIFAI_WORKFLOW_URL not set. Image analysis will be disabled.")
                    return
                
                try:
                    # Initialize user with the PAT
                    self.user = User(pat=self.pat)
                    self.is_available = True
                    current_app.logger.info(f"Clarifai image analysis service initialized successfully with workflow URL: {self.workflow_url}")
                except Exception as init_error:
                    current_app.logger.error(f"Clarifai client initialization error: {str(init_error)}")
                    return
            else:
                current_app.logger.warning(f"Unsupported provider: {provider}. Image analysis will be disabled.")
        except Exception as e:
            current_app.logger.error(f"Failed to initialize image analysis service: {str(e)}")
        
    def analyze_image(self, image_bytes=None, image_url=None):
        """
        Analyze an image using the configured AI provider.
        
        Args:
            image_bytes: Binary image data (if provided)
            image_url: URL to the image (if image_bytes not provided)
            
        Returns:
            dict: Dictionary containing analysis results or fallback message
        """
        # Early return if service is not available
        if not self.is_available:
            return self._create_fallback_response("Image analysis service is not available")
            
        # Ensure we have either bytes or URL
        if not image_bytes and not image_url:
            return self._create_fallback_response("Either image_bytes or image_url must be provided")
            
        # Analyze based on the provider
        try:
            if self.provider == "clarifai":
                return self._analyze_with_clarifai_workflow(image_bytes, image_url)
            else:
                return self._create_fallback_response(f"Unsupported provider: {self.provider}")
        except Exception as e:
            current_app.logger.error(f"Image analysis error: {str(e)}")
            return self._create_fallback_response(f"Analysis failed: {str(e)}")
    
    def _analyze_with_clarifai_workflow(self, image_bytes=None, image_url=None):
        """
        Analyze an image using Clarifai's workflow API.
        
        Args:
            image_bytes: Binary image data (if provided)
            image_url: URL to the image (if image_bytes not provided)
            
        Returns:
            dict: Dictionary containing analysis results
        """
        try:
            # Create workflow using URL and PAT
            workflow = Workflow(url=self.workflow_url, pat=self.pat)
            current_app.logger.info(f"Created workflow with URL: {self.workflow_url}")
            
            # Determine whether to use image bytes or URL
            if image_bytes:
                current_app.logger.info("Predicting using image bytes")
                response = workflow.predict_by_bytes(image_bytes, input_type="image")
            else:
                current_app.logger.info(f"Predicting using URL: {image_url}")
                response = workflow.predict_by_url(image_url, input_type="image")
            
            # Process results from the new structure
            description = None
            concepts = []
            
            # Extract data from response
            if hasattr(response, 'results') and response.results:
                result = response.results[0]  # Get the first result
                current_app.logger.info(f"Got result with {len(result.outputs) if hasattr(result, 'outputs') else 0} outputs")
                
                if hasattr(result, 'outputs') and result.outputs:
                    for output in result.outputs:
                        if hasattr(output, 'data'):
                            # Extract text/caption data
                            if hasattr(output.data, 'text'):
                                description = output.data.text.raw
                                current_app.logger.info(f"Extracted caption: {description}")
                            
                            # Extract concept data
                            if hasattr(output.data, 'concepts'):
                                for concept in output.data.concepts:
                                    if concept.value > 0.5:  # Filter by confidence
                                        concepts.append({
                                            "name": concept.name,
                                            "value": concept.value,
                                            "model": output.model.id if hasattr(output, 'model') else "unknown"
                                        })
            
            # If no description was found but we have concepts, generate one
            if not description and concepts:
                description = self.generate_description(concepts)
                
            # Sort concepts by confidence
            concepts = sorted(concepts, key=lambda x: x['value'], reverse=True)
            
            return {
                "description": description,
                "concepts": concepts,
                "workflow_url": self.workflow_url,
                "raw_response": str(response)  # Convert to string to avoid serialization issues
            }
            
        except Exception as e:
            current_app.logger.error(f"Clarifai workflow API error: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            return self._create_fallback_response(f"Clarifai workflow error: {str(e)}")
    
    def _create_fallback_response(self, error_message):
        """Create a standard fallback response"""
        current_app.logger.warning(f"Using fallback response: {error_message}")
        return {
            "description": None,
            "concepts": [],
            "error": error_message,
            "using_fallback": True
        }
    
    def generate_description(self, concepts, max_concepts=5):
        """
        Generate a human-readable description from the top concepts.
        
        Args:
            concepts: List of concept dictionaries with 'name' and 'value'
            max_concepts: Maximum number of concepts to include in the description
            
        Returns:
            str: A human-readable description
        """
        if not concepts:
            return None
            
        # Sort concepts by confidence and take the top ones
        sorted_concepts = sorted(concepts, key=lambda x: x['value'], reverse=True)
        top_concepts = sorted_concepts[:max_concepts]
        
        # Create a simple description
        concept_names = [c['name'] for c in top_concepts]
        
        if len(concept_names) == 1:
            return f"This image appears to be a {concept_names[0]}."
        elif len(concept_names) == 2:
            return f"This image appears to contain {concept_names[0]} and {concept_names[1]}."
        else:
            return "This image appears to contain " + ", ".join(concept_names[:-1]) + f", and {concept_names[-1]}."


# Legacy alias for backward compatibility
ClarifaiService = ImageAnalysisService