const Submit = async (event) => {
event.preventDefault();
const form = document.getElementById('submit-form');
const formData = new FormData(form);

const json = {};

formData.forEach((value, key) => {
  json[key] = value;
});
console.log(json);

let newImage = await fetch(post_url,  {
  method: 'POST',
  body: formData
}).then(response => response.json())
  .then(data =>{
    console.log(data);
    const { success } = data;
    if(!success){
        console.log({"Errors":data})
    }
    else{
        const { tokens } = data
        const { access } = tokens
        const { refresh } = tokens

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        
      if(access && refresh){
          window.location.href = home_url
      }
    }
  })
  .catch(error => { console.error(error) })
}