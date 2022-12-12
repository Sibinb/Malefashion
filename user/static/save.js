const arr=[]
const save_btn=document.getElementById("s").addEventListener("click",(e)=>{
  const otp =document.getElementById("show")
  e.preventDefault()
  const form= document.getElementById("save-form")
  const dta=new FormData(form)
         $.ajax({
             url: "profile",
             type: "POST",
             enctype: 'multipart/form-data',
             data:dta,
             success: function (data) {
              if(data['otp']){
               otp.innerHTML=`<label id="label" class="labels">Enter the OTP</label><input type="number" name="otp" class="form-control" placeholder="enter the otp" value="">`
              }else if(data['otp_error']){
                console.log("enter")
               const error = document.getElementById("label")
               error.innerHTML="Invalid otp"
               error.style.color="red"
              }
              else{
                otp.innerHTML=""
                const Toast = Swal.mixin({
                  toast: true,
                  position: 'top-end',
                  showConfirmButton: false,
                  timer: 1000,
                  didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                  }
                })
                
                Toast.fire({
                  icon: 'success',
                  title: 'Profile saved successfully'
                })
              } 
             },
             error: function (err) {
                alert(err);
             },
             cache: false,
            contentType: false,
            processData: false,
         }); 
})

function image(){
  const img =document.getElementById("image")
  img.innerHTML=`<label class="labels">Choose the profile pic</label><input  accept="image/*" name="img" type="file">`
}







