function addCouseSyllabusRows(){ 
	var table = document.getElementById('Couse_Syllabus');
	var rowCount = table.rows.length;
	var cellCount = table.rows[0].cells.length; 
	var row = table.insertRow(rowCount);
	for(var i =0; i < cellCount; i++){
		var cell = 'cell'+i;
		cell = row.insertCell(i);
		var copycel = document.getElementById('col'+i).innerHTML;
		cell.innerHTML=copycel;
	
	}
}

function deleteCouseSyllabusRows(){
	var table = document.getElementById('Couse_Syllabus');
	var rowCount = table.rows.length;
	if(rowCount > '2'){
		var row = table.deleteRow(rowCount-1);
		rowCount--;
	}
	else{
		alert('There should be atleast one row');
	}
}

function addCouseModuleRows(){ 
	var table = document.getElementById('Couse_Module');
	var rowCount = table.rows.length;
	var cellCount = table.rows[0].cells.length; 
	var row = table.insertRow(rowCount);
	for(var i =0; i <= cellCount; i++){
		var cell = 'cell0'+i;
		cell = row.insertCell(i);
		var copycel = document.getElementById('col0'+i).innerHTML;
		cell.innerHTML=copycel;
		if(i == 1){ 
			var fileinput = document.getElementById('col01').getElementsByTagName('input'); 
			for(var j = 0; j <= fileinput.length; j++) { 
				fileinput[j].type = 'file'				
			}
		}
	
	}
}


function deleteCouseModuleRows(){
	var table = document.getElementById('Couse_Module');
	var rowCount = table.rows.length;
	if(rowCount > '2'){
		var row = table.deleteRow(rowCount-1);
		rowCount--;
	}
	else{
		alert('There should be atleast one row');
	}
}

function addCouseTimeTableRows(){ 
	var table = document.getElementById('Couse_Time_Table');
	var rowCount = table.rows.length;
	var cellCount = table.rows[0].cells.length; 
	var row = table.insertRow(rowCount);
	for(var i =0; i <= cellCount; i++){
		var cell = 'cell00'+i;
		cell = row.insertCell(i);
		var copycel = document.getElementById('col00'+i).innerHTML;
		cell.innerHTML=copycel;		
	
	}
}

function deleteCouseTimeTableRows(){
	var table = document.getElementById('Couse_Time_Table');
	var rowCount = table.rows.length;
	if(rowCount > '2'){
		var row = table.deleteRow(rowCount-1);
		rowCount--;
	}
	else{
		alert('There should be atleast one row');
	}
}

function addCouseExamRows(){ 
	var table = document.getElementById('Couse_Exam_Table');
	var rowCount = table.rows.length;
	var cellCount = table.rows[0].cells.length; 
	var row = table.insertRow(rowCount);
	for(var i =0; i <= cellCount; i++){
		var cell = 'cell000'+i;
		cell = row.insertCell(i);
		var copycel = document.getElementById('col000'+i).innerHTML;
		cell.innerHTML=copycel;	
	
	}
}

function deleteCouseExamRows(){
	var table = document.getElementById('Couse_Exam_Table');
	var rowCount = table.rows.length;
	if(rowCount > '2'){
		var row = table.deleteRow(rowCount-1);
		rowCount--;
	}
	else{
		alert('There should be atleast one row');
	}
}


