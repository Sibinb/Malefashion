
const alertBox = document.getElementById("alert-box")
const imageBox = document.getElementById("image-box")
const imageForm = document.getElementById("image-form")
const confirmBtn = document.getElementById("confirm-btn")
const img_div=document.getElementById("img_div")

const csrf = document.getElementsByName('csrfmiddlewaretoken')
const arr=[]
function man(id){
    alertBox.innerHTML = ""
    const input = document.getElementById(id)
    const img_data = input.files[0]
    const url = URL.createObjectURL(img_data)

    imageBox.innerHTML = `<img src="${url}" id="image" width="500px">`
    var $image = $('#image')
    console.log($image)
    img_div.classList.add("img_div");
    confirmBtn.classList.remove("confirm_cls");

    $image.cropper({
        aspectRatio: 30 /40,
        crop: function(event) {
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);
        }
    });
    var cropper = $image.data('cropper');
    confirmBtn.addEventListener('click', (e)=>{
        e.preventDefault()
        cropper.getCroppedCanvas().toBlob((blob) => {
            arr[id]=blob
            console.log(url)
            img_div.classList.remove("img_div");
            confirmBtn.classList.add("confirm_cls");
            imageBox.innerHTML=""
            console.log('confirmed') 
            console.log(arr) 
        })
    })
}


document.getElementById("sub").onclick=function sub(e){
    e.preventDefault()
    const fd = new FormData(imageForm );
            fd.append('img1',arr[0], 'my-image1.png');
            fd.append('img2',arr[1], 'my-image2.png');
            fd.append('img3',arr[2], 'my-image3.png');
            fd.append('img4',arr[3], 'my-image4.png');

            $.ajax({
                type:'POST',
                url: imageForm.action,
                enctype: 'multipart/form-data',
                data: fd,
                success: function(response){
                    console.log('success', response)
                    location.href="product"
                },
                error: function(error){
                    console.log('error', error)
                    alertBox.innerHTML = `<div class="alert alert-danger" role="alert">Ups...something went wrong</div>`
                },
                cache: false,
                contentType: false,
                processData: false,
            })
}
document.getElementById("edit-sub").onclick=function sub(e){
    e.preventDefault()
    const fd = new FormData(imageForm );
    if(arr[0]&&arr[1]&&arr[2]&&arr[3]){
        alert("good")
    }else{
        alert("Bad")
    }
            fd.append('img1',arr[0], 'my-image1.png');
            fd.append('img2',arr[1], 'my-image2.png');
            fd.append('img3',arr[2], 'my-image3.png');
            fd.append('img4',arr[3], 'my-image4.png');

            $.ajax({
                type:'POST',
                url: imageForm.action,
                enctype: 'multipart/form-data',
                data: fd,
                success: function(response){
                    console.log('success', response)
                    location.href="product"
                },
                error: function(error){
                    console.log('error', error)
                    alertBox.innerHTML = `<div class="alert alert-danger" role="alert">Ups...something went wrong</div>`
                },
                cache: false,
                contentType: false,
                processData: false,
            })
}


