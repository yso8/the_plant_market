/*
document.querySelector("button.add-to-cart").addEventListener("click", event => {
    let test = document.querySelector("button.add-to-cart").value
    console.log(test)
})
*/

let buttons = document.querySelectorAll('.add-to-cart');

function getCookie(csrftoken) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", () => {

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        let selectedButton = buttons[i].value
        console.log("Selected button " + selectedButton)

        const request = new Request(
            '/add/test/',
    {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin', // Do not send CSRF token to another domain.
            body: JSON.stringify({
                'selectedProduct' : selectedButton,
            }),
         }
        );
        fetch(request)
            .then(res => res.json())
            .then(data => {
                console.log(data)
            })
    })
}
