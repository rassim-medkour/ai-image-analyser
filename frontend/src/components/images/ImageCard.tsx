import React, { useState } from "react";
import { Image } from "../../types";

interface ImageCardProps {
    image: Image;
}

const CARD_SIZE = 500;

const ImageCard: React.FC<ImageCardProps> = ({ image }) => {
    const [showModal, setShowModal] = useState(false);

    return (
        <div
            className="image-card"
            style={{
                width: CARD_SIZE,
                minHeight: CARD_SIZE + 60,
                boxShadow: "0 2px 8px #0001",
                borderRadius: 10,
                background: "#fff",
                padding: 14,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                cursor: "pointer",
                transition: "box-shadow 0.2s",
            }}
            onClick={() => setShowModal(true)}
        >
            <img
                src={image.s3_url}
                alt={image.original_filename}
                style={{
                    width: CARD_SIZE - 20,
                    height: CARD_SIZE - 20,
                    objectFit: "cover",
                    borderRadius: 8,
                    background: "#f3f3f3",
                }}
                loading="lazy"
            />
            <div style={{ marginTop: 10, width: "100%", textAlign: "center" }}>
                <div
                    style={{
                        fontWeight: 600,
                        fontSize: "1.05em",
                        whiteSpace: "nowrap",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                    }}
                    title={image.original_filename}
                >
                    {image.original_filename}
                </div>
                {image.ai_description && (
                    <div
                        style={{
                            fontSize: "0.93em",
                            color: "#555",
                            marginTop: 4,
                            minHeight: 32,
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                            display: "-webkit-box",
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: "vertical",
                        }}
                        title={image.ai_description}
                    >
                        {image.ai_description}
                    </div>
                )}
            </div>
            {showModal && (
                <div
                    style={{
                        position: "fixed",
                        top: 0,
                        left: 0,
                        width: "100vw",
                        height: "100vh",
                        background: "rgba(0,0,0,0.8)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        zIndex: 2000,
                    }}
                    onMouseDown={e => {
                        // Only close if the click is on the backdrop, not the image
                        if (e.target === e.currentTarget) setShowModal(false);
                    }}
                >
                    <img
                        src={image.s3_url}
                        alt={image.original_filename}
                        style={{
                            maxWidth: "90vw",
                            maxHeight: "90vh",
                            borderRadius: 10,
                            boxShadow: "0 4px 24px #0008",
                            background: "#fff",
                        }}
                        onMouseDown={e => e.stopPropagation()}
                    />
                </div>
            )}
        </div>
    );
};

export default ImageCard;
