import React from "react";
import { Image } from "../../types";

interface ImageCardProps {
    image: Image;
}

const ImageCard: React.FC<ImageCardProps> = ({ image }) => {
    return (
        <div className="image-card">
            <img
                src={image.s3_url}
                alt={image.original_filename}
                style={{ width: "100%", aspectRatio: "1/1", objectFit: "cover", borderRadius: "0.5rem" }}
            />
            <div style={{ marginTop: "0.5rem" }}>
                <strong>{image.original_filename}</strong>
                {image.ai_description && (
                    <p style={{ fontSize: "0.9em", color: "var(--pico-muted-color)" }}>{image.ai_description}</p>
                )}
            </div>
        </div>
    );
};

export default ImageCard;
