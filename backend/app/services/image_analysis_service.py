"""
Image Analysis Service: Provides integration with AI vision APIs for image content analysis.
This service implements the adapter pattern to abstract various AI vision service providers.
Currently implements Clarifai workflow-based image analysis with fallback mechanisms.
The design supports extending to other AI providers in the future.
"""
import sys
import traceback
from flask import current_app

# Conditional import with error handling to prevent application crashes
# when optional dependencies are not installed
try:
    # Clarifai client imports - version 11.2+ uses this API structure
    from clarifai.client.user import User
    from clarifai.client.workflow import Workflow
    CLARIFAI_AVAILABLE = True
except ImportError as e:
    current_app.logger.error(f"Clarifai import error: {str(e)}, paths: {sys.path}")
    CLARIFAI_AVAILABLE = False


class ImageAnalysisService:
    """
    Generic image analysis service that implements an adapter pattern for AI vision providers.
    Currently supports Clarifai workflows as the default provider, with proper error handling
    and graceful degradation when services are unavailable.
    """
    
    def __init__(self, provider="clarifai"):
        """
        Initialize the image analysis service with the specified provider.
        
        Args:
            provider (str): The AI provider to use ('clarifai' by default)
                           Could be extended to support other providers
        """
        self.provider = provider
        self.pat = None  # Personal Access Token for Clarifai
        self.is_available = False
        self.workflow_url = None
        self.user = None
        
        # Provider-specific initialization with comprehensive error handling
        try:
            if provider == "clarifai":
                # Check if Clarifai package is available
                if not CLARIFAI_AVAILABLE:
                    current_app.logger.warning("Clarifai package is not installed. Image analysis will be disabled.")
                    return
                
                # Get authentication credentials from configuration
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
                    # Initialize Clarifai user with the PAT for authentication
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
        Primary public method to analyze an image using the configured AI provider.
        Supports both binary image data and URL-based image analysis.
        
        Args:
            image_bytes: Binary image data as bytes (takes precedence if both provided)
            image_url: URL to the image (used if image_bytes not provided)
            
        Returns:
            dict: Structured dictionary containing:
                - description: Generated textual description of the image
                - concepts: List of identified concepts/tags with confidence scores
                - error: Error message if analysis failed
                - using_fallback: Boolean indicating if this is a fallback response
        """
        # Early validation to prevent unnecessary processing
        if not self.is_available:
            return self._create_fallback_response("Image analysis service is not available")
            
        # Input validation - require at least one source of image data
        if not image_bytes and not image_url:
            return self._create_fallback_response("Either image_bytes or image_url must be provided")
            
        # Provider-specific analysis with error handling
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
        Internal method to analyze an image using Clarifai's workflow API.
        Workflow allows chaining multiple AI models for comprehensive analysis.
        
        Args:
            image_bytes: Binary image data (if provided)
            image_url: URL to the image (used if image_bytes not provided)
            
        Returns:
            dict: Structured response with description, concepts, and metadata
        """
        try:
            # Initialize workflow with the configured URL and authentication
            workflow = Workflow(url=self.workflow_url, pat=self.pat)
            current_app.logger.info(f"Created workflow with URL: {self.workflow_url}")
            
            # Select the appropriate prediction method based on available inputs
            if image_bytes:
                current_app.logger.info("Predicting using image bytes")
                response = workflow.predict_by_bytes(image_bytes, input_type="image")
            else:
                current_app.logger.info(f"Predicting using URL: {image_url}")
                response = workflow.predict_by_url(image_url, input_type="image")
            
            # Process results from the workflow response
            description = None
            concepts = []
            
            # Extract data from potentially nested response structure
            if hasattr(response, 'results') and response.results:
                result = response.results[0]  # Get the first result
                current_app.logger.info(f"Got result with {len(result.outputs) if hasattr(result, 'outputs') else 0} outputs")
                
                if hasattr(result, 'outputs') and result.outputs:
                    for output in result.outputs:
                        if hasattr(output, 'data'):
                            # Extract text/caption data (typically from LLM or captioning models)
                            if hasattr(output.data, 'text'):
                                description = output.data.text.raw
                                current_app.logger.info(f"Extracted caption: {description}")
                            
                            # Extract concept data (typically from classification models)
                            if hasattr(output.data, 'concepts'):
                                for concept in output.data.concepts:
                                    # Filter out low-confidence predictions (threshold: 0.5)
                                    if concept.value > 0.5:
                                        concepts.append({
                                            "name": concept.name,
                                            "value": concept.value,
                                            "model": output.model.id if hasattr(output, 'model') else "unknown"
                                        })
            
            # Generate a description from concepts if none was provided by the models
            if not description and concepts:
                description = self.generate_description(concepts)
                
            # Sort concepts by confidence score for better presentation
            concepts = sorted(concepts, key=lambda x: x['value'], reverse=True)
            
            return {
                "description": description,
                "concepts": concepts,
                "workflow_url": self.workflow_url,
                "raw_response": str(response)  # Serialized to string to avoid JSON serialization issues
            }
            
        except Exception as e:
            # Comprehensive error logging with stack trace for debugging
            current_app.logger.error(f"Clarifai workflow API error: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            return self._create_fallback_response(f"Clarifai workflow error: {str(e)}")
    
    def _create_fallback_response(self, error_message):
        """
        Create a standardized fallback response structure for error cases.
        This ensures consistent error handling throughout the application.
        
        Args:
            error_message: Descriptive error message
            
        Returns:
            dict: Structured fallback response with error details and empty results
        """
        current_app.logger.warning(f"Using fallback response: {error_message}")
        return {
            "description": None,
            "concepts": [],
            "error": error_message,
            "using_fallback": True
        }
    
    def generate_description(self, concepts, max_concepts=5):
        """
        Generate a natural language description from identified concepts.
        Creates human-readable text based on the confidence-ranked concepts.
        
        Args:
            concepts: List of concept dictionaries with 'name' and 'value' (confidence score)
            max_concepts: Maximum number of concepts to include in the description
            
        Returns:
            str: A human-readable description sentence
        """
        if not concepts:
            return None
            
        # Sort concepts by confidence and take the top ones
        sorted_concepts = sorted(concepts, key=lambda x: x['value'], reverse=True)
        top_concepts = sorted_concepts[:max_concepts]
        
        # Extract just the concept names for the description
        concept_names = [c['name'] for c in top_concepts]
        
        # Generate appropriate natural language based on number of concepts
        if len(concept_names) == 1:
            return f"This image appears to be a {concept_names[0]}."
        elif len(concept_names) == 2:
            return f"This image appears to contain {concept_names[0]} and {concept_names[1]}."
        else:
            return "This image appears to contain " + ", ".join(concept_names[:-1]) + f", and {concept_names[-1]}."


# Legacy alias for backward compatibility with code that may import the original name
ClarifaiService = ImageAnalysisService