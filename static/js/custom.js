/* Search Card Script */
/* ------------------ */

const queryParams = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
});

// // keep coach name input search value
const coach_name_q_input = document.querySelector('[name="coach_name_q"]')
coach_name_q_input.value = queryParams.coach_name_q;

// // keep coach speciality input search value
const coach_speciality_q_input = document.querySelector('[name="coach_speciality_q"]')
coach_speciality_q_input.value = queryParams.coach_speciality_q;

// // keep min price input search value
const min_price_q_input = document.querySelector('[name="min_price_q"]')
if (queryParams.min_price_q == null){
    min_price_q_input.value = 0;
}
else{
    min_price_q_input.value = queryParams.min_price_q;
    let min_price_q_output = document.querySelector('#min_price_q_output')
    min_price_q_output.value = queryParams.min_price_q
}

// // keep max price input search value
const max_price_q_input = document.querySelector('[name="max_price_q"]')
if (queryParams.max_price_q == null){
    max_price_q_input.value = 1000;
}
else{
    max_price_q_input.value = queryParams.max_price_q;
    let max_price_q_output = document.querySelector('#max_price_q_output')
    max_price_q_output.value = queryParams.max_price_q
}

// // keep date input search value
const available_date_q_input = document.querySelector('[name="available_date_q"]')
if (queryParams.available_date_q !== null){
    available_date_q_input.value = queryParams.available_date_q;
}

/* ---------------------------------------------------------------------------- */



