// logout.js

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("logout-link").addEventListener("click", function(event) {
        event.preventDefault(); // Prevent the default behavior of the link
        
        // Create a form element
        var form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "{% url 'logout' %}");
        
        // Create a CSRF token input field
        var csrfToken = document.createElement("input");
        csrfToken.setAttribute("type", "hidden");
        csrfToken.setAttribute("name", "csrfmiddlewaretoken");
        csrfToken.setAttribute("value", "{{ csrf_token }}");
        
        // Append the CSRF token input field to the form
        form.appendChild(csrfToken);
        
        // Append the form to the document body and submit it
        document.body.appendChild(form);
        form.submit();
    });
});
