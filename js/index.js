
$(document).ready(function() {
	// Makes sure the dataTransfer information is sent when we
	// Drop the item in the drop box.
	jQuery.event.props.push('dataTransfer');
	
	// Get all of the data URIs and put them in an array
	var dataArray = [];
		
	// Bind the drop event to the dropzone.
	$('#dropfiles').bind('drop', function(e) {
		// Stop the default action, which is to redirect the page
		// To the dropped file
		var files = e.dataTransfer.files;
		
		// For each file
		$.each(files, function(index, file) {
			// Start a new instance of FileReader
			var fileReader = new FileReader();
				// When the filereader loads initiate a function
				fileReader.onload = (function(file) {
					return function(e) { 
						// Push the data URI into an array
						dataArray.push({name : file.name, value : this.result});
						$.post('./js/i-upload.php', dataArray[0], function(data) {
							// to stat page
							$('.introduce-drop').hide();
							$('.commit-group').show();
							$('.converted-content').html(data);
						});
					}; 
				})(files[index]);
				
			// For data URI purposes
			fileReader.readAsDataURL(file);
		});
	});
		
	// Just some styling for the drop file container.
	$('#dropfiles').bind('dragenter', function() {
		$(this).css({'box-shadow' : 'inset 0px 0px 20px rgba(0, 0, 0, 0.1)', 'border' : '2px dashed #bb2b2b'});
		return false;
	});
	
	$('#dropfiles').bind('drop', function() {
		$(this).css({'box-shadow' : 'none', 'border' : '2px dashed rgba(0,0,0,0.2)'});
		return false;
	});
	
	$('.convert-filename').change(function(){
		var files = this.files;
    var file = files[0];
    name = file.name;
    size = file.size;
    type = file.type;
    
		$.each(files, function(index, file) {
			// Start a new instance of FileReader
			var fileReader = new FileReader();
				// When the filereader loads initiate a function
				fileReader.onload = (function(file) {
					return function(e) { 
						// Push the data URI into an array
						dataArray.push({name : file.name, value : this.result});
						$.post('./js/i-upload.php', dataArray[0], function(data) {
							// to stat page
							$('.introduce-drop').hide();
							$('.commit-group').show();
							$('.results-group').show();		
							$('.converted-content').html(data);
						});
					}; 
				})(files[index]);
				
			// For data URI purposes
			fileReader.readAsDataURL(file);
		});    
	});
});
