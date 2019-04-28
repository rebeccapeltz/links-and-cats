document.addEventListener("DOMContentLoaded", event => {
  if (window.location.href.indexOf("index") > -1) {
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
  }

  //category manager
  if (window.location.href.indexOf("manage_categories") > -1) {

    let catManBtns = document.querySelectorAll(".cat-man-btn")
    for (let btn of catManBtns) {
      btn.addEventListener('click', function (event) {
        let i = this.dataset.idx;
        let catOrigDescription = document.querySelector(`#cat-orig${i}`).innerHTML
        let catNewDescription = document.querySelector(`#cat-new${i}`).value

        let tempForm = document.createElement('form');
        tempForm.setAttribute('action', '/update_category');
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
    }

    //click on fa-edit and show input and submit button
    // upd-cat{{loop.index0}}
    function showHideUpdate(ev) {
      // this ought to keep t-daddy from getting the click.
      ev.stopPropagation();
      // alert("event propagation halted.");
      let idx = this.dataset.idx;
      // get matching update controls
      let editSpan = document.querySelector(`#upd-cat${idx}`)
      // toggle show/hide
      editSpan.classList.toggle("none")
      editSpan.classList.toggle("show-inline")
    }
    let editIcons = document.querySelectorAll(".fa-edit");
    for (let icon of editIcons) {
      icon.addEventListener("click", showHideUpdate, false)
    }

    function deleteCat(ev) {
      ev.stopPropagation();
      let i = this.dataset.idx;
      let catDescTxt = document.querySelector(`#cat-orig${i}`).innerHTML
      let tempForm = document.createElement('form');

      let input = document.createElement('input');
      input.setAttribute('type', 'text');
      input.setAttribute('name', 'desc-input');
      input.setAttribute('value', catDescTxt);
      tempForm.appendChild(input);

      tempForm.setAttribute('action', '/delete_category');
      tempForm.setAttribute('method', 'post');
      tempForm.setAttribute('hidden', 'true');
      document.body.appendChild(tempForm);
      tempForm.submit();
    }
    //click on fa-trash-alt and get orignal value and delete it
    let delIcons = document.querySelectorAll(".fa-trash-alt");
    for (let icon of delIcons) {
      icon.addEventListener("click", deleteCat, false)
    }
  }


})