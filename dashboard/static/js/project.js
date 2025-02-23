async function handleImageUpload(event) {
    const file = event.target.files[0];
    console.log('Starting image upload process...');
    console.log('Selected file:', file ? file.name : 'No file selected');
    
    if (!file) {
        console.warn('No file selected, aborting upload');
        return;
    }

    // Get CSRF token from the form
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log('CSRF token retrieved successfully');

    try {
        // 1. Convert image to base64
        console.log('Starting image to base64 conversion...');
        const reader = new FileReader();
        const base64Image = await new Promise((resolve, reject) => {
            reader.onload = () => {
                console.log('Image successfully converted to base64');
                resolve(reader.result.split(',')[1]);
            };
            reader.onerror = error => {
                console.error('Error converting image to base64:', error);
                reject(error);
            };
            reader.readAsDataURL(file);
        });
        console.log('Base64 image length:', base64Image.length);
        
        // Update the preview image
        const preview = document.getElementById('thumbnail_preview');
        preview.src = `data:${file.type};base64,${base64Image}`;
        console.log('Preview image updated successfully');

        // 2. Analyze the image
        console.log('Sending image for analysis...');
        const analyzeResponse = await fetch('/dashboard/analyze-image/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                image_base64: base64Image,
                image_type: file.type
            })
        });

        const responseData = await analyzeResponse.json();
        console.log('Analysis response received:', responseData);
        
        if (!analyzeResponse.ok) {
            console.error('Image analysis failed with status:', analyzeResponse.status);
            throw new Error(responseData.message || 'Image analysis failed');
        }
        
        // 3. Populate the description fields with the analysis
        const descriptionAr = document.getElementById('description_ar');
        const descriptionFr = document.getElementById('description_fr');
        
        if (responseData.status === 'success' && responseData.data?.description) {
            // Use Marked.js to convert Markdown to HTML
            const formattedDescription = marked.parse(responseData.data.description);

            // Use TinyMCE API to set the content
            if (tinymce.get('description_ar')) {
                tinymce.get('description_ar').setContent(formattedDescription);
            } else {
                document.getElementById('description_ar').value = formattedDescription;
            }
            
            if (tinymce.get('description_fr')) {
                tinymce.get('description_fr').setContent(formattedDescription);
            } else {
                document.getElementById('description_fr').value = formattedDescription;
            }
            
            console.log('Description fields populated successfully in TinyMCE editors');
        } else {
            console.warn('No valid description data received');
            throw new Error('No valid description data received from server');
        }

        console.log('Image upload and analysis completed successfully');
    } catch (error) {
        console.error('Error processing image:', error);
        alert('Error processing image: ' + error.message);
    }
}

// Example usage with file input
document.getElementById('imageInput').addEventListener('change', handleImageUpload);