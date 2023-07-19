const dragArea = document.querySelector('.drag-area');
const dragText = document.querySelector('.header');
const cropsDropdown = document.querySelector('#crops-dropdown');
const diseaseHolder = document.querySelector('#diseaseHolder');

let button = document.querySelector('.button');
let input = document.querySelector('input');

let file;

cropsDropdown.addEventListener("DOMContentLoaded", function() {
    console.log("Logging")
  });

function loadModels(){
    console.log("Loading models");
    const access = localStorage.getItem('access_token');
    fetch(modelsUrl,  {
    headers: {Authorization: 'Bearer ' + access},
     })
     .then(response => response.json())
     .then(data =>{
        const { models } = data;
        for(var crop in models){
            var opt = document.createElement('option');
            opt.value = models[crop];
            opt.innerHTML = models[crop];
            opt.style = "font-size: small;"
            cropsDropdown.appendChild(opt);
        }
     })
     .catch(error => { console.error(error) });
}
loadModels();
button.onclick = () => {
    input.click();
};

input.addEventListener('change', function(){
    file = this.files[0];
    dragArea.classList.add('active');
    displayFile();
})

dragArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    dragText.textContent = 'Release to Upload';
    dragArea.classList.add('active');
});

dragArea.addEventListener('dragleave', () => {
    dragText.textContent = 'Drag & Drop';
    dragArea.classList.remove('active');
});

dragArea.addEventListener('drop', (event) => {
    event.preventDefault();

    file = event.dataTransfer.files[0]; 
    displayFile();
});

function displayFile(){
let fileType = file.type;
    

    let validExtensions = ['image/jpeg', 'image/jpg', 'image/png'];

    if(validExtensions.includes(fileType)){
        let fileReader = new FileReader();

        fileReader.onload = () => {
            let fileURL = fileReader.result;
            
            let imgTag = `<img src="${fileURL}" alt= "">`;
            dragArea.innerHTML = imgTag;
        };
        fileReader.readAsDataURL(file);
    }
    else{
        alert('Unsupported format!');
        dragArea.classList.remove('active');
    }
}

const createImage = async (event) => {
    event.preventDefault()
    let image = file
    let formData = new FormData()

    formData.append('img_path', image)
    formData.append('plant_type', 'Potato')
    const access = localStorage.getItem('access_token')

    let newImage = await fetch(createUrl,  {
       headers: {Authorization: 'Bearer ' + access},
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data);
        const { _complete } = data;
        if(_complete){
            const { disease } = data;
            diseaseHolder.innerHTML = disease;
        }
    })
    .catch(error => { console.error(error) })
}