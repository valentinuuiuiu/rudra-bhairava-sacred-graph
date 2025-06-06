document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('id_images');
    const previewContainer = document.getElementById('image-preview');
    const dropZone = document.getElementById('drop-zone');
    const maxFileSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

    function handleFiles(files) {
        Array.from(files).forEach((file, index) => {
            // Validate file size and type
            if (file.size > maxFileSize) {
                showError(`Imaginea ${file.name} este prea mare. Dimensiunea maximă este 5MB.`);
                return;
            }
            if (!allowedTypes.includes(file.type)) {
                showError(`Formatul imaginii ${file.name} nu este acceptat. Formatele acceptate sunt: JPEG, PNG, GIF, WEBP.`);
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = createPreviewElement(e.target.result, index);
                previewContainer.appendChild(preview);
            };
            reader.readAsDataURL(file);
        });

        // Update main image indicators
        updateMainImageIndicators();
    }

    function createPreviewElement(src, index) {
        const wrapper = document.createElement('div');
        wrapper.className = 'relative w-32 h-32 m-2 group';
        wrapper.setAttribute('data-index', index);

        const img = document.createElement('img');
        img.src = src;
        img.className = 'w-full h-full object-cover rounded-lg shadow-md';

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity';
        removeBtn.innerHTML = '×';
        removeBtn.onclick = function() {
            wrapper.remove();
            updateMainImageIndicators();
        };

        const mainLabel = document.createElement('span');
        mainLabel.className = 'absolute bottom-1 left-1 bg-green-500 text-white text-xs px-2 py-1 rounded';
        mainLabel.textContent = 'Principal';
        if (index === 0) mainLabel.classList.remove('hidden');
        else mainLabel.classList.add('hidden');

        wrapper.appendChild(img);
        wrapper.appendChild(removeBtn);
        wrapper.appendChild(mainLabel);

        // Make images draggable for reordering
        wrapper.draggable = true;
        wrapper.addEventListener('dragstart', handleDragStart);
        wrapper.addEventListener('dragover', handleDragOver);
        wrapper.addEventListener('drop', handleDrop);

        return wrapper;
    }

    function updateMainImageIndicators() {
        const previews = previewContainer.querySelectorAll('[data-index]');
        previews.forEach((preview, idx) => {
            const mainLabel = preview.querySelector('span');
            if (idx === 0) mainLabel.classList.remove('hidden');
            else mainLabel.classList.add('hidden');
            preview.setAttribute('data-index', idx);
        });
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-2';
        errorDiv.role = 'alert';
        errorDiv.textContent = message;
        
        const closeButton = document.createElement('button');
        closeButton.className = 'absolute top-0 right-0 px-4 py-3';
        closeButton.innerHTML = '×';
        closeButton.onclick = () => errorDiv.remove();
        
        errorDiv.appendChild(closeButton);
        previewContainer.parentElement.insertBefore(errorDiv, previewContainer);
        
        setTimeout(() => errorDiv.remove(), 5000);
    }

    // Drag and drop functionality
    function handleDragStart(e) {
        e.dataTransfer.setData('text/plain', e.target.getAttribute('data-index'));
        e.target.classList.add('opacity-50');
    }

    function handleDragOver(e) {
        e.preventDefault();
    }

    function handleDrop(e) {
        e.preventDefault();
        const sourceIndex = e.dataTransfer.getData('text/plain');
        const sourceElement = document.querySelector(`[data-index="${sourceIndex}"]`);
        const targetElement = e.target.closest('[data-index]');
        
        if (sourceElement && targetElement) {
            // Swap elements
            const tempHtml = sourceElement.innerHTML;
            sourceElement.innerHTML = targetElement.innerHTML;
            targetElement.innerHTML = tempHtml;
            
            // Update main image indicators
            updateMainImageIndicators();
        }
        
        sourceElement.classList.remove('opacity-50');
    }

    // Event listeners
    imageInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-primary');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('border-primary');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-primary');
        handleFiles(e.dataTransfer.files);
    });
});
