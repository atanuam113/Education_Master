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
	document.getElementById("totalSyllabusRows").value = rowCount;
	
	
}

function deleteCouseSyllabusRows(){
	var table = document.getElementById('Couse_Syllabus');
	var rowCount1 = table.rows.length;
	if(rowCount1 > '2'){
		var row = table.deleteRow(rowCount1-1);
		rowCount1--;
	}
	else{
		alert('There should be atleast one row');
	}
	document.getElementById("totalSyllabusRows").value = rowCount1-1;
	
}

function addCouseModuleRows(){ 
	var table = document.getElementById('Couse_Module');
	var rowCount2 = table.rows.length;
	var cellCount = table.rows[0].cells.length; 
	var row = table.insertRow(rowCount2);
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
	
	document.getElementById("totalModuleRows").value = rowCount2;
	
}


function deleteCouseModuleRows(){
	var table = document.getElementById('Couse_Module');
	var rowCount3 = table.rows.length;
	if(rowCount3 > '2'){
		var row = table.deleteRow(rowCount3-1);
		rowCount3--;
	}
	else{
		alert('There should be atleast one row');
	}
	document.getElementById("totalModuleRows").value = rowCount3-1;
	
}

function addCouseTimeTableRows(){ 
	var table = document.getElementById('Couse_Time_Table');
	var rowCount4 = table.rows.length;
	var cellCount = table.rows[0].cells.length; 
	var row = table.insertRow(rowCount4);
	for(var i =0; i <= cellCount; i++){
		var cell = 'cell00'+i;
		cell = row.insertCell(i);
		var copycel = document.getElementById('col00'+i).innerHTML;
		cell.innerHTML=copycel;		
	
	}
	document.getElementById("totalTimeTableRows").value = rowCount4;
	
}

function deleteCouseTimeTableRows(){
	var table = document.getElementById('Couse_Time_Table');
	var rowCount5 = table.rows.length;
	if(rowCount5 > '2'){
		var row = table.deleteRow(rowCount5-1);
		rowCount5--;
	}
	else{
		alert('There should be atleast one row');
	}
	document.getElementById("totalTimeTableRows").value = rowCount5-1;
	
}

function addCouseExamRows(){ 
	var table = document.getElementById('Couse_Exam_Table');
	var rowCount6 = table.rows.length;
	var cellCount = table.rows[0].cells.length; 
	var row = table.insertRow(rowCount6);
	for(var i =0; i <= cellCount; i++){
		var cell = 'cell000'+i;
		cell = row.insertCell(i);
		var copycel = document.getElementById('col000'+i).innerHTML;
		cell.innerHTML=copycel;	
	
	}
	document.getElementById("totalExamTableRows").value = rowCount6;
	
}

function deleteCouseExamRows(){
	var table = document.getElementById('Couse_Exam_Table');
	var rowCount7 = table.rows.length;
	if(rowCount7 > '2'){
		var row = table.deleteRow(rowCount7-1);
		rowCount7--;
	}
	else{
		alert('There should be atleast one row');
	}
	document.getElementById("totalExamTableRows").value = rowCount7-1;
	
}

$('#Add_course_form').submit(function () {
	$('.menu1Input').each(function(){
		var menu_entry = "";

		$(this).find('.courseModuleInput').each(function(){
			menu_entry = menu_entry + this.value + ","
		})
		$('#Add_course_form').append('<input type="hidden" name="menu_entries" value="'+ menu_entry +'" />')

	})

	$('.menu2Input').each(function(){
		var menu_entry1 = "";
		var file,files,fileLength,fileList;
		$(this).find('.IndModuleInput').each(function(){
			files  = this.files;
			fileList = $('.files');
			fileLength = files.length;
			read=new FileReader();
        	read.readAsBinaryString( file );
			
			menu_entry1 = menu_entry1 + this.value + ","
			alert("menu_entry1:"+menu_entry1);
		})
		$('#Add_course_form').append('<input type="hidden" name="menu_module" value="'+ menu_entry1 +'" />')

	})
	$('.manu3Input').each(function(){
		var menu_entry2 = "";

		$(this).find('.courseSyllabusInput').each(function(){
			menu_entry2 = menu_entry2 + this.value + ","
		})
		$('#Add_course_form').append('<input type="hidden" name="menu_syllabus" value="'+ menu_entry2 +'" />')

	})
	$('.menu4Input').each(function(){
		var menu_entry4 = "";

		$(this).find('.courseExamInput').each(function(){
			menu_entry4 = menu_entry4 + this.value + ","
		})
		$('#Add_course_form').append('<input type="hidden" name="menu_exam" value="'+ menu_entry4 +'" />')

	})
})

