const dragArea = document.querySelector('.drag-area');
const dragText = document.querySelector('.header');

let button = document.querySelector('.button');
let input = document.querySelector('input');

let file;



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
    // console.log('File is inside the drag area');
});

dragArea.addEventListener('dragleave', () => {
    dragText.textContent = 'Drag & Drop';
    dragArea.classList.remove('active');
    // console.log('File left the drag area');
});

dragArea.addEventListener('drop', (event) => {
    event.preventDefault();

    file = event.dataTransfer.files[0]; // how many files to upload
    // console.log(file);
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
    const imageEndpoint = 'http://127.0.0.1/detection/create'
    // let imageInput = document.querySelector('#inputImage');
    // let fileInput = document.querySelector('.container .drag-area input[type="file"]');

    let image = file
    let formData = new FormData()

    formData.append('img_path', image)
    formData.append('plant_type', 'Potato')
    const access = localStorage.getItem('access_token')

    let newImage = await fetch(imageEndpoint,  {
       headers: {Authorization: 'Bearer ' + access},
      method: 'POST',
      body: formData
    }).then(response => response.json()).catch(error => { console.error(error) })
}