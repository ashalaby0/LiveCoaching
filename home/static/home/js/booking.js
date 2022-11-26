let activateHour = (evt) => {
  evt.target.checked = true;
  document.querySelector('#book_button').disabled = false
};


let getAvailHours = (url) => {
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
      newRadioLabel.setAttribute("class", "btn btn-outline-primary");
      newRadioLabel.setAttribute("for", `option${i}`);
      newRadioLabel.textContent = element;

      newRadio.addEventListener("click", (event) => activateHour(event));
      availHoursUl.append(newRadioLabel);
    });
  }
};
document
  .querySelector("#sesion-date")
  .addEventListener("change", updateAvailHours);