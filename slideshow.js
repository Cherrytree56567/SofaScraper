function plusSlides(n, containerId) {
  const container = document.querySelector(`[data-container="${containerId}"]`);
  if (container) {
    const slides = container.getElementsByClassName("mySlides");
    let slideIndex = parseInt(container.dataset.slideIndex) || 1;
  
    slideIndex += n;
    if (slideIndex > slides.length) slideIndex = 1; // Wrap to first slide
    if (slideIndex < 1) slideIndex = slides.length; // Wrap to last slide
  
    container.dataset.slideIndex = slideIndex; // Store the updated index
    showSlides(slides, slideIndex);
  }
}
  
function showSlides(slides, index) {
  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[index - 1].style.display = "block"; // Show the active slide
}