"""
Analysis Strategies: Implements different strategies for image analysis
following the Strategy design pattern.
"""
from abc import ABC, abstractmethod
from flask import current_app


class AnalysisStrategy(ABC):
    """Abstract base class for image analysis strategies"""
    
    @abstractmethod
    def analyze(self, analysis_service, image_bytes=None, image_url=None, **kwargs):
        """
        Analyze an image using a specific strategy
        
        Args:
            analysis_service: The service to use for analysis
            image_bytes: Binary image data (optional)
            image_url: URL to the image (optional)
            
        Returns:
            dict: Analysis result
        """
        pass


class UrlAnalysisStrategy(AnalysisStrategy):
    """Strategy for analyzing images via URL"""
    
    def analyze(self, analysis_service, image_bytes=None, image_url=None, **kwargs):
        if not image_url:
            current_app.logger.warning("URL strategy selected but no URL provided")
            return {"using_fallback": True, "error": "No URL provided"}
            
        current_app.logger.info(f"Analyzing image via URL: {image_url}")
        return analysis_service.analyze_image(image_url=image_url)


class BytesAnalysisStrategy(AnalysisStrategy):
    """Strategy for analyzing images via binary data"""
    
    def analyze(self, analysis_service, image_bytes=None, image_url=None, **kwargs):
        if not image_bytes:
            current_app.logger.warning("Bytes strategy selected but no bytes provided")
            return {"using_fallback": True, "error": "No image data provided"}
            
        current_app.logger.info("Analyzing image via bytes")
        return analysis_service.analyze_image(image_bytes=image_bytes)


class FallbackAnalysisStrategy(AnalysisStrategy):
    """Strategy that tries URL first, then falls back to bytes if needed"""
    
    def analyze(self, analysis_service, image_bytes=None, image_url=None, **kwargs):
        if image_url:
            try:
                current_app.logger.info(f"Attempting URL-based analysis: {image_url}")
                result = analysis_service.analyze_image(image_url=image_url)
                
                # If the result indicates a fallback was used or no description was found,
                # try bytes instead
                if result.get('using_fallback', False) or not result.get('description'):
                    current_app.logger.warning(
                        f"URL analysis failed or returned no results: {result.get('error')}, trying bytes"
                    )
                    if image_bytes:
                        return analysis_service.analyze_image(image_bytes=image_bytes)
                    else:
                        current_app.logger.error("No image bytes available for fallback")
                
                return result
                
            except Exception as e:
                current_app.logger.warning(f"URL analysis failed with error: {str(e)}, trying bytes")
                if image_bytes:
                    try:
                        return analysis_service.analyze_image(image_bytes=image_bytes)
                    except Exception as bytes_error:
                        current_app.logger.error(f"Bytes analysis also failed: {str(bytes_error)}")
                        return {
                            "using_fallback": True, 
                            "error": f"Both URL and bytes analysis failed: {str(e)} / {str(bytes_error)}"
                        }
                else:
                    return {"using_fallback": True, "error": f"URL analysis failed and no bytes provided: {str(e)}"}
        elif image_bytes:
            current_app.logger.info("No URL provided, using bytes directly")
            return analysis_service.analyze_image(image_bytes=image_bytes)
        else:
            return {"using_fallback": True, "error": "Neither URL nor bytes provided"}