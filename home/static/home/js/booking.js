let activateHour = async (evt) => {
  evt.target.checked = true;
  let validPromoCode = await checkPromoCode()
      console.log(validPromoCode)
      if (['empty', 'valid'].includes(validPromoCode)){
        document.querySelector('#book_button').disabled = false
      }
};


let getAvailHours = (url) => {
  let _date = document.querySelector("#session-date").value
  url = url.replace('datePlaceHolder',_date)
  return fetch(url, {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      return data.av_hours;
    });
};

let updateAvailHours = async (evt) => {
  let url = evt.currentTarget.attributes["data-url"].value;
  let availHoursUl = document.querySelector("#avail-hours");
  let availHours = await getAvailHours(url);
  console.log(availHours);
  if (availHours.length === 0) {
    availHoursUl.innerHTML =
      "<p class='text-center text-danger w-100'>Not Available...</p>";
  } else {
    availHoursUl.textContent = "";
    availHours.forEach((element, i) => {
      let newRadio = document.createElement("input");
      newRadio.setAttribute("type", "radio");
      newRadio.setAttribute("class", "btn-check");
      newRadio.setAttribute("name", "sessionHour");
      newRadio.setAttribute("id", `option${i}`);
      newRadio.setAttribute("value", element);
      availHoursUl.append(newRadio);

      let newRadioLabel = document.createElement("label");
      newRadioLabel.setAttribute("class", "btn custom-btn-outline-primary");
      newRadioLabel.setAttribute("for", `option${i}`);
      newRadioLabel.textContent = element;

      newRadio.addEventListener("click", (event) => activateHour(event));
      
      availHoursUl.append(newRadioLabel);
    });
  }
};


document
  .querySelector("#session-date")
  .addEventListener("change", updateAvailHours);


let checkPromoCode = async function(){
  promoCodeInput = document.querySelector('#pCode');
  promoCode = promoCodeInput.value;
  promoCodeValidationUrl = promoCodeInput.attributes['data-url'].value;
  if (promoCode == ''){
    return 'empty'
  }


  let response = await fetch(
    promoCodeValidationUrl,
    {method: 'POST',body: JSON.stringify({'promoCode':promoCode})}
    )
  let responseObj = await response.json()
  console.log(`validation result:  ${responseObj.result}`)
  if (!['empty', 'valid'].includes(responseObj.result) && document.querySelector('#book_button').disabled == false){
    document.querySelector('#book_button').disabled = true
    console.log('disabled')
  }
    return responseObj.result

}

document.querySelector('#pCode').addEventListener('keyup', checkPromoCode)