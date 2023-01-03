document.querySelector("#pay-button").addEventListener("click", event =>{
    let formData = new FormData();

    let card_holder = document.querySelector("#id_name").value;
    let card_number = document.querySelector("#id_card_number").value;
    let expiration_date = document.querySelector("#id_expiration_date").value;
    let cvv = document.querySelector("#id_cvv").value;

    formData.append('card_holder', card_holder);
    formData.append('card_number', card_number);
    formData.append('expiration_date', expiration_date);
    formData.append('cvv', cvv);

    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const request = new Request('/payment-check/',
        {
                method: 'POST',
                headers: {'X-CSRFToken': csrf_token},
                mode: 'same-origin', // Do not send CSRF token to another domain.
                body: formData
            });

    fetch(request)
        .then(response => response.json())
        .then(result => console.log(result))
        .catch(err => {
            console.log(err)
        });
})