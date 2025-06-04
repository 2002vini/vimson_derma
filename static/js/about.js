document.addEventListener("DOMContentLoaded", function () {
    // Make image maps responsive
    const imageMap = document.querySelector('img[usemap]');
    if (imageMap) {
        // Load rwdImageMaps.js functionality (if necessary)
        window.addEventListener("resize", resizeImageMap);
        resizeImageMap();
    }

    function resizeImageMap() {
        const img = document.querySelector('img[usemap]');
        if (!img) return;
        
        const width = img.naturalWidth;
        const height = img.naturalHeight;
        const newWidth = img.clientWidth;
        const scale = newWidth / width;

        document.querySelectorAll('area').forEach(area => {
            const coords = area.dataset.originalCoords || area.getAttribute('coords');
            area.dataset.originalCoords = coords;
            const coordsArray = coords.split(',').map(coord => Math.round(coord * scale));
            area.setAttribute('coords', coordsArray.join(','));
        });
    }    
    const modalImage = document.getElementById('modalImage');
modalImage.addEventListener('show.bs.modal', function (event) {
  const area = event.relatedTarget; // Get the clicked area
  const imgSrc = area.getAttribute('data-img'); // Fetch image from data-img attribute
  const title=area.getAttribute('title');
  document.getElementById('popup-img').src = imgSrc; // Set modal image source
  document.getElementById('modal-title').innerHTML = title;
});
});