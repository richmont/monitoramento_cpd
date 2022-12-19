// Validating Empty Field
function check_empty() {
    if (document.getElementById('id_nome').value == "" || document.getElementById('id_local').value == "" || document.getElementById('id_IP').value == "" || document.getElementById('id_modelo').value == "") {
    alert("Fill All Fields !");
    } else {
    document.getElementById('form').submit();
    alert("Form Submitted Successfully...");
    }
    }
    //Function To Display Popup
    function div_show() {
        formulario_cadastro = document.getElementById("form-cadastro-impressora");
        formulario_cadastro.classList.remove("oculto");
        formulario_cadastro.classList.add("exibir");
    }
    //Function to Hide Popup
    function div_hide(){
        formulario_cadastro = document.getElementById("form-cadastro-impressora");
        formulario_cadastro.classList.remove("exibir");
        formulario_cadastro.classList.add("oculto");
    }
    
    