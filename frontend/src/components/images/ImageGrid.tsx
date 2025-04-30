import React from "react";
import { Image } from "../../types";
import ImageCard from "./ImageCard";

interface ImageGridProps {
    images: Image[];
}

const ImageGrid: React.FC<ImageGridProps> = ({ images }) => {
    return (
        <div
            className="image-grid"
            style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
                gap: "1.5rem",
                marginTop: "2rem"
            }}
        >
            {images.map((img) => (
                <ImageCard key={img.id} image={img} />
            ))}
        </div>
    );
};

export default ImageGrid;
