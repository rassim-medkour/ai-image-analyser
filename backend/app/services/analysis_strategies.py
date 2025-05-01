"""
Analysis Strategies: Implements the Strategy design pattern for image analysis.
This module defines several concrete strategies for analyzing images using different approaches:
1. URL-based analysis: Uses pre-signed URLs to analyze images directly from storage
2. Bytes-based analysis: Uses binary image data for analysis
3. Fallback analysis: Attempts URL-based strategy first, then falls back to bytes-based if needed

This pattern allows for flexible image analysis approaches while encapsulating the complexity
of each strategy's implementation details.
"""
from abc import ABC, abstractmethod
from flask import current_app


class AnalysisStrategy(ABC):
    """
    Abstract base class for image analysis strategies.
    Defines the interface that all concrete analysis strategies must implement.
    Follows the Strategy design pattern to enable runtime selection of analysis algorithms.
    """
    
    @abstractmethod
    def analyze(self, analysis_service, image_bytes=None, image_url=None, **kwargs):
        """
        Abstract method to analyze an image using a specific strategy.
        Must be implemented by all concrete strategy classes.
        
        Args:
            analysis_service: The AI service instance to use for analysis
            image_bytes: Binary image data (optional)
            image_url: URL to the image (optional)
            **kwargs: Additional strategy-specific parameters
            
        Returns:
            dict: Analysis result with structured data
        """
        pass


class UrlAnalysisStrategy(AnalysisStrategy):
    """
    Concrete strategy that analyzes images via URL.
    This is typically more efficient as it doesn't require transferring image data twice,
    but depends on the AI service having network access to the image URL.
    """
    
    def analyze(self, analysis_service, image_bytes=None, image_url=None, **kwargs):
        """
        Analyze an image using only its URL.
        
        Args:
            analysis_service: The AI service to use for analysis
            image_bytes: Binary image data (ignored in this strategy)
            image_url: URL to the image (required)
            **kwargs: Additional parameters
            
        Returns:
            dict: Analysis results or error response if URL is missing
        """
        if not image_url:
            current_app.logger.warning("URL strategy selected but no URL provided")
            return {"using_fallback": True, "error": "No URL provided"}
            
        current_app.logger.info(f"Analyzing image via URL: {image_url}")
        return analysis_service.analyze_image(image_url=image_url)


class BytesAnalysisStrategy(AnalysisStrategy):
    """
    Concrete strategy that analyzes images via binary data.
    This approach is more reliable as it doesn't depend on network accessibility
    of the image URL, but requires transferring the image data twice.
    """
    
    def analyze(self, analysis_service, image_bytes=None, image_url=None, **kwargs):
        """
        Analyze an image using its binary data.
        
        Args:
            analysis_service: The AI service to use for analysis
            image_bytes: Binary image data (required)
            image_url: URL to the image (ignored in this strategy)
            **kwargs: Additional parameters
            
        Returns:
            dict: Analysis results or error response if bytes are missing
        """
        if not image_bytes:
            current_app.logger.warning("Bytes strategy selected but no bytes provided")
            return {"using_fallback": True, "error": "No image data provided"}
            
        current_app.logger.info("Analyzing image via bytes")
        return analysis_service.analyze_image(image_bytes=image_bytes)


class FallbackAnalysisStrategy(AnalysisStrategy):
    """
    Advanced strategy that combines URL and bytes approaches for maximum reliability.
    First attempts to analyze using URL (more efficient), then falls back to bytes
    if URL analysis fails or returns empty results. This provides the best balance
    between efficiency and reliability.
    """
    
    def analyze(self, analysis_service, image_bytes=None, image_url=None, **kwargs):
        """
        Analyze an image using the fallback approach (URL first, then bytes).
        Implements a comprehensive error handling and fallback mechanism.
        
        Args:
            analysis_service: The AI service to use for analysis
            image_bytes: Binary image data (used as fallback)
            image_url: URL to the image (tried first if available)
            **kwargs: Additional parameters
            
        Returns:
            dict: Analysis results from either URL or bytes analysis
        """
        if image_url:
            try:
                # First attempt: URL-based analysis
                current_app.logger.info(f"Attempting URL-based analysis: {image_url}")
                result = analysis_service.analyze_image(image_url=image_url)
                
                # Check for failure indicators in the result
                # If the result indicates a fallback was used or no description was found,
                # try bytes instead for more reliable results
                if result.get('using_fallback', False) or not result.get('description'):
                    current_app.logger.warning(
                        f"URL analysis failed or returned no results: {result.get('error')}, trying bytes"
                    )
                    # Only attempt bytes analysis if we have the image data
                    if image_bytes:
                        return analysis_service.analyze_image(image_bytes=image_bytes)
                    else:
                        current_app.logger.error("No image bytes available for fallback")
                
                # URL analysis succeeded
                return result
                
            except Exception as e:
                # Error handling for URL analysis failure
                current_app.logger.warning(f"URL analysis failed with error: {str(e)}, trying bytes")
                # Fallback to bytes analysis if available
                if image_bytes:
                    try:
                        return analysis_service.analyze_image(image_bytes=image_bytes)
                    except Exception as bytes_error:
                        # Both methods failed - comprehensive error reporting
                        current_app.logger.error(f"Bytes analysis also failed: {str(bytes_error)}")
                        return {
                            "using_fallback": True, 
                            "error": f"Both URL and bytes analysis failed: {str(e)} / {str(bytes_error)}"
                        }
                else:
                    return {"using_fallback": True, "error": f"URL analysis failed and no bytes provided: {str(e)}"}
        elif image_bytes:
            # No URL available, use bytes directly
            current_app.logger.info("No URL provided, using bytes directly")
            return analysis_service.analyze_image(image_bytes=image_bytes)
        else:
            # Neither input method available - invalid request
            return {"using_fallback": True, "error": "Neither URL nor bytes provided"}