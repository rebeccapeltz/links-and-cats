document.addEventListener("DOMContentLoaded", event => {
  let option1 = document.querySelector("#option1")
  let option2 = document.querySelector("#option2")
  let option3 = document.querySelector("#option3")
  let publicRow = document.querySelector(".public-row")
  let privateRow = document.querySelector(".private-row")
  if (option1 && option2 && option3) {
    option1.addEventListener("click", event => {
      event.stopPropagation()
      publicRow.style.display = "flex"
      privateRow.style.display = "flex"
    })
    option2.addEventListener("click", event => {
      event.stopPropagation()
      publicRow.style.display = "flex"
      privateRow.style.display = "none"
    })
    option3.addEventListener("click", event => {
      event.stopPropagation()
      publicRow.style.display = "none"
      privateRow.style.display = "flex"
    })
  }

  //category manager
  let catManBtns = document.querySelectorAll(".cat-man-btn")
  for (let btn of catManBtns) {
    btn.addEventListener('click', function (event) {
      let i = $(this).data('idx');
      let catOrigDescription = document.querySelector(`#cat-orig${i}`).innerHTML
      let catNewDescription = document.querySelector(`#cat-new${i}`).value
      // alert(catNewDescription.value)
      let tempForm = document.createElement('form');
      tempForm.setAttribute('action', '/manage_categories');
      tempForm.setAttribute('method', 'post');
      tempForm.setAttribute('hidden', 'true');
      //add original value
      let descOrigInput = document.createElement('input');
      descOrigInput.setAttribute('type', 'text');
      descOrigInput.setAttribute('name', 'desc-input-orig');
      descOrigInput.setAttribute('value', catOrigDescription);
      tempForm.appendChild(descOrigInput);
      //add new value
      let descNewInput = document.createElement('input');
      descNewInput.setAttribute('type', 'text');
      descNewInput.setAttribute('name', 'desc-input-new');
      descNewInput.setAttribute('value', catNewDescription);
      tempForm.appendChild(descNewInput);

      document.body.appendChild(tempForm);
      tempForm.submit();
    })

    //click on fa-edit and show input and submit button

    //click on fa-trash-alt and get orignal value and delete it
  }
})