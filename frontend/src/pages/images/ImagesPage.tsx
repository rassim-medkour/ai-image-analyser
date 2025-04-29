import React, { useEffect, useState } from "react";
import { getUserImages } from "../../api/images";
import { Image } from "../../types";
import ImageGrid from "../../components/images/ImageGrid";

const ImagesPage: React.FC = () => {
    const [images, setImages] = useState<Image[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchImages = async () => {
            try {
                setLoading(true);
                const imgs = await getUserImages();
                setImages(imgs);
            } catch (err) {
                setError("Failed to load images.");
            } finally {
                setLoading(false);
            }
        };
        fetchImages();
    }, []);

    if (loading) return <div>Loading images...</div>;
    if (error) return <div className="text-error">{error}</div>;

    return (
        <main>
            <h1>Your Images</h1>
            {images.length === 0 ? (
                <p>No images found.</p>
            ) : (
                <ImageGrid images={images} />
            )}
        </main>
    );
};

export default ImagesPage;
