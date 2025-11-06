<!-- Add this to your existing HTML file -->
<!-- Replace the current script section with this enhanced version -->

<script>
    // Existing functionality remains the same...
    
    // Enhanced affiliate link handling
    document.querySelectorAll('.add-to-cart').forEach((button, index) => {
        button.addEventListener('click', function() {
            const products = [
                'https://www.amazon.com/dp/B09G9FPHY6?tag=your-affiliate-id',
                'https://www.amazon.com/dp/B08N5LNQCX?tag=your-affiliate-id', 
                'https://www.amazon.com/dp/B09JQMJHXY?tag=your-affiliate-id',
                'https://www.amazon.com/dp/B0CHX3QBCH?tag=your-affiliate-id',
                'https://www.amazon.com/dp/B091J3NY3S?tag=your-affiliate-id',
                'https://www.amazon.com/dp/B094WKNQ8F?tag=your-affiliate-id'
            ];
            
            const affiliateUrl = products[index] || '#';
            window.open(affiliateUrl, '_blank');
            
            // Show notification
            const notification = document.createElement('div');
            notification.innerHTML = `
                <div style="position: fixed; top: 80px; right: 20px; background: #FFD814; color: #0F1111; padding: 15px 20px; border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); z-index: 1000; font-weight: bold;">
                    Redirecting to product page...
                </div>
            `;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        });
    });

    // Contact form handling (if you add a contact form)
    function handleContactForm(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);
        
        // In a real implementation, this would send to a Netlify function
        alert('Thank you for your message! In a real implementation, this would be sent to your email.');
        e.target.reset();
    }
    
    // Add event listener for contact form if it exists
    const contactForm = document.querySelector('#contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
</script>

