const Login = async (event) => {
  event.preventDefault()
  const loginEndpoint = 'http://127.0.0.1/api/user/signin/'
  const email = document.getElementById('inputEmail').value
  const password = document.getElementById('inputPassword').value

  const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

  const formData = JSON.stringify({"email": email, "password": password, "csrfmiddlewaretoken" : csrf});
  let newImage = await fetch(loginEndpoint,  {
    headers: {"content-type": "application/json"},
    method: 'POST',
    body: formData
  }).then(response => response.json())
  .then(data =>{
    console.log(data);
    const { sucess } = data;
    if(!sucess){
        console.log({"Errors":data})
    }
    else{
        const { tokens } = data
        const { access } = tokens
        const { refresh } = tokens

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        
        console.log("Access")
        console.log(access)
        console.log("Refresh")
        console.log(refresh)
        //if(access && refresh){
        //    window.location.href = "{% url 'website:home' %}"
        //}
    }
  })
  .catch(error => { console.error(error) })

}
