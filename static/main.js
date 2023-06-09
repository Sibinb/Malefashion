
function addcart(proid, state) {
  $.ajax({
    url: "add_cart",
    type: "GET",
    data: { id: proid, st: state },
    success: function (data) {
      console.log(data);
      if (data == 0) {
        alert("there is an error man.....");
      } else {
        location.href = data;
      }
    },
    error: function (err) {
      alert(err);
    },
  });
}

function remove_frm_cart(proid) {
  Swal.fire({
    title: "Do you want to remove this product from cart?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, delete it!",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire("Deleted!", "Your file has been deleted.", "success");
      const myTimeout = setTimeout(reponse, 1500);
      function reponse() {
        $.ajax({
          url: "remove_frm_cart",
          type: "GET",
          data: { id: proid },
          success: function (data) {
            if (data == 0) {
              alert("there is an error man.....");
            } else {
              location.href = data;
            }
          },
          error: function (err) {
            alert(err);
          },
        });
      }
    }
  });
}

function count(num, proid,qunty) {
  let display = document.getElementById(proid);
  let current_qunty = Number(display.innerHTML);
  if (current_qunty < 2 && num == -1) {
    $.ajax({
      url: "remove_frm_cart",
      type: "GET",
      data: { id: proid },
      success: function (data) {
        if (data == 0) {
          alert("there is an error man.....");
        } else {
          location.href = data;
        }
      },
      error: function (err) {
        alert(err);
      },
    });
  } else {
    if(current_qunty + num>qunty){
      console.log(current_qunty + num,"val",qunty);
      alert("Product is out of stock")
      return 0
    }else{
    console.log("working");
    display.innerHTML = current_qunty + num;
    let value = display.innerHTML;
    $.ajax({
        url: "quant_add",
        type: "GET",
        data: { id: proid, quant: value },
        success: function (data) {
          let tot_price = document.getElementById(proid + "qn");
          tot_price.innerHTML = data.prodo_price;
          let total_pr = document.getElementById("total_price");
          total_pr.innerHTML = "&#8377;" + data.total_price;
        },
        error: function (err) {
          alert(err);
        },
      });
    }
  }
}

function add_wishlist(proid) {
  $.ajax({
    url: "add_to_wishlist",
    type: "GET",
    data: { id: proid },
    success: function (data) {
      let heart = document.getElementById(proid + "heart");
      if (data == 1) {
        heart.innerHTML = `<i class="fa fa-heart" style="font-size:24px;color: red;">`;
      } else {
        heart.innerHTML = `<i class="fa fa-heart-o" style="font-size:24px;">`;
      }
    },
    error: function (err) {
      alert(err);
    },
  });
}
function add_wishlist_from(proid) {
  $.ajax({
    url: "add_to_wishlist",
    type: "GET",
    data: { id: proid },
    success: function (data) {
      let heart = document.getElementById(proid + "heart");
      if (data == 1) {
        const Toast = Swal.mixin({
          toast: true,
          position: "top-end",
          showConfirmButton: false,
          timer: 1000,
          didOpen: (toast) => {
            toast.addEventListener("mouseenter", Swal.stopTimer);
            toast.addEventListener("mouseleave", Swal.resumeTimer);
          },
        });
        Toast.fire({
          icon: "success",
          title: "Product added to wishlist",
        });
      } else {
        const Toast = Swal.mixin({
          toast: true,
          position: "top-end",
          showConfirmButton: false,
          timer: 1000,
          didOpen: (toast) => {
            toast.addEventListener("mouseenter", Swal.stopTimer);
            toast.addEventListener("mouseleave", Swal.resumeTimer);
          },
        });

        Toast.fire({
          icon: "success",
          title: "Product added to wishlist ",
        });
      }
    },
    error: function (err) {
      alert(err);
    },
  });
}

function cancelorder(proid) {
  Swal.fire({
    title: "Do you want to cancel the order?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire("Deleted!", "Your order has been cancelled.", "success");
      const myTimeout = setTimeout(reponse, 1000);
      function reponse() {
        $.ajax({
          url: "cancel-order",
          type: "GET",
          data: { id: proid },
          success: function (data) {
            location.href = data;
          },
          error: function (err) {
            alert(err);
          },
        });
      }
    }
  });
}
const form = document.getElementById("myForm_12");
document.getElementById("cash").addEventListener("click", function (event) {
  event.preventDefault();
  var serializedData = $("form").serialize();
  $.ajax({
    url: form.action,
    type: "POST",
    data: serializedData,
    success: function (data) {
      if (data.cod) {
        location.href = "confirm";
      } else {
        var options = {
          key: "rzp_test_NGcaol52IYnJlE",
          amount: data.res.amount,
          currency: "INR",
          name: "Acme Corp",
          description: "Test Transaction",
          image: "https://example.com/your_logo",
          order_id: data.res.id,
          handler: function (response) {
            $.ajax({
              url: "placeorder!2",
              type: "GET",
              data: {},
              success: function (data) {
                location.href = data;
              },
              error: function (err) {
                alert(err);
              },
            });
          },
          prefill: {
            name: data.addr.name,
            email: data.addr.email,
            contact: data.addr.mobileno,
          },
          notes: {
            address: "Razorpay Corporate Office",
          },
          theme: {
            color: "#3399cc",
          },
        };
        var rzp1 = new Razorpay(options);
        rzp1.open();
      }
    },
    error: function (err) {
      alert("fill the details");
    },
  });
});

function coupon(num) {
  let idi;
  let dta;
  let id_id;
  if (num == 0) {
    const ido = document.getElementById("couponid");
    idi = ido.value;
    dta = ido.innerText;
    id_id = 0;
  } else {
    const ido = document.getElementById("code");
    idi = ido.value;
    dta = ido.value;
    id_id = 1;
  }
  $.ajax({
    url: "apply_cop",
    type: "GET",
    data: { coup: idi, id: id_id },
    success: function (data) {
      if (data.error) {
        const err = document.getElementById("error");
        err.innerHTML = data.error;
      } else {
        const sh = document.getElementById("cop_price");
        const to = document.getElementById("tot");
        const err = document.getElementById("error");
        err.innerHTML = "";
        sh.innerHTML = `${dta}<span>-&#8377;${data.sum}</span>`;
        to.innerHTML = `Total <span>&#8377;${data.tot}</span>`;
        const Toast = Swal.mixin({
          toast: true,
          position: "top-end",
          showConfirmButton: false,
          timer: 1000,
          didOpen: (toast) => {
            toast.addEventListener("mouseenter", Swal.stopTimer);
            toast.addEventListener("mouseleave", Swal.resumeTimer);
          },
        });

        Toast.fire({
          icon: "success",
          title: "Coupon applied sucessfully",
        });
      }
    },
    error: function (err) {
      alert(err);
    },
  });
}

function returnorder(proid) {
  Swal.fire({
    title: "Do you want to return the order?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire("Returned!", "Your order will return soon.", "success");
      const myTimeout = setTimeout(reponse, 1000);
      function reponse() {
        $.ajax({
          url: "return-order",
          type: "GET",
          data: { id: proid },
          success: function (data) {
            location.href = data;
          },
          error: function (err) {
            alert(err);
          },
        });
      }
    }
  });
}

function create_coupon() {
  const form = document.getElementById("coupon-form");
  const fd = new FormData(form);
  $.ajax({
    url: form.action,
    type: "POST",
    enctype: "multipart/form-data",
    data: fd,
    success: function (data) {
      const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 1000,
        didOpen: (toast) => {
          toast.addEventListener("mouseenter", Swal.stopTimer);
          toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
      });

      Toast.fire({
        icon: "success",
        title: "Coupon added successfully",
      });
      location.href = form.action;
    },
    error: function (err) {
      alert(err);
    },
    cache: false,
    contentType: false,
    processData: false,
  });
}

function remove_frm_wishlist(proid) {
    Swal.fire({
      title: "Do you want to remove this product from wishlist?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, delete it!",
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire("Deleted!", "Your file has been deleted.", "success");
        const myTimeout = setTimeout(reponse, 1000);
        function reponse() {
          $.ajax({
            url: "remove_frm_wishlist",
            type: "GET",
            data: { id: proid },
            success: function (data) {
              if (data == 0) {
                alert("Sorry there is a little problem");
              } else {
                location.href = data;
              }
            },
            error: function (err) {
              alert(err);
            },
          });
        }
      }
    });
  }

  function sort(){
    const val= document.getElementById("sort_val").value
    location.href="s!p!"+val
  }