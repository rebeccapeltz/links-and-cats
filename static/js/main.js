document.addEventListener("DOMContentLoaded",event=>{
  let option1 = document.querySelector("#option1")
  let option2 = document.querySelector("#option2")
  let option3 = document.querySelector("#option3")
  let publicRow = document.querySelector(".public-row")
  let privateRow = document.querySelector(".private-row")
  if (option1 && option2 && option3){
  option1.addEventListener("click",event=>{
    event.stopPropagation()
    publicRow.style.display = "flex"
    privateRow.style.display = "flex"
  })
  option2.addEventListener("click",event=>{
    event.stopPropagation()
    publicRow.style.display = "flex"
    privateRow.style.display = "none"
  })
  option3.addEventListener("click",event=>{
    event.stopPropagation()
    publicRow.style.display = "none"
    privateRow.style.display = "flex"
  })
}
})