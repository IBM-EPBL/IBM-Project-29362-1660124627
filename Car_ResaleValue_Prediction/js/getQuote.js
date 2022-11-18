// api url
//const api_url =	"https://private-anon-5cdb0e8df4-carsapi1.apiary-mock.com/manufacturers";
//const api_url = "https://parseapi.back4app.com/classes/Car_Model_List?count=1&limit=10000";
const api_url = "https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getModels";
const api_url_models = "https://parseapi.back4app.com/classes/Car_Model_List_";
// Defining async function
const options = {
	headers: {
		'X-RapidAPI-Key': '208141881bmshc7d1fe0defc3916p1f6cbdjsn20a6b0279138',
		'X-RapidAPI-Host': 'car-data.p.rapidapi.com'
	}
}
const options1 = {
	headers: {
		'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z', // This is the fake app's application id
		'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW', // This is the fake app's readonly master key
	  }
	}
async function getapi(url) {
	
	// Storing response
	const response = await fetch(url);
	
	// Storing data in form of JSON
	var data = await response.json();
	console.log(data);
	if (response) {
		hideloader();
	}
	show(data);
}
function hideloader() {
    document.getElementById('loading').style.display = 'none';
}
// Calling that async function
getapi(api_url);

// Function to define innerHTML for HTML table
function show(data) {

	let tab = "<select class='form-control' id='select-brand' onchange='getModels(api_url_models)' name='brands'><option valu=''>Select a Brand</option>";
	// Loop to access all rows
	for (let r of data.Makes) {
		tab += `
	<option value="${r}">${r}</option>
`;
	}
    tab += `</select>`;
	// Setting innerHTML as tab variable
	document.getElementById("getBrands").innerHTML = tab;
}
function hideloader1() {
    document.getElementById('loading1').style.display = 'none';
}
async function getModels(url) {
	console.log("url after "+url);
	// Storing response
	var make = document.getElementById('select-brand').value;
	make = make.toLowerCase();
	make = make.charAt(0).toUpperCase()+make.slice(1);
	console.log(make);
	const response = await fetch(url+make+'?count=1&limit=1000',options1);
	
	// Storing data in form of JSON
	var data = await response.json();
	console.log(data);
	if (response) {
		hideloader1();
	}
	showModels(data);
}

function showModels(data) {

	let tab = "<select class='form-control' id='select-model' name='model'>";
	const key = 'Model';

	const arrayUniqueByKey = [...new Map(data.results.map(item =>
	[item[key], item])).values()];

	// Loop to access all rows
	for (let r of arrayUniqueByKey) {
		tab += `
	<option value="${r.Model}">${r.Model}</option>
`;
	}
    tab += `</select>`;
	// Setting innerHTML as tab variable
	document.getElementById("getModels").innerHTML = tab;
}