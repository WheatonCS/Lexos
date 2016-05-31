# jquery.dataTables.areaselect

Extension of **[jquery.dataTables](https://www.datatables.net/)** plugin for area selection.

![](http://acuisinier.com/images/jquery.dataTables.multiselect.png)

## Documentation & demo

> For code sample check out the *index.html* file or go to [live demo](http://acuisinier.com/demo/jquery.dataTables.areaselect).
  
**Minimal browser compatibility**

Web browser|Version 
---|---
Chrome|Ok
Firefox|v3.5
IE|v9
Opera|v10
Safari|v4

**Dependencies**

> **jQuery v1.11.3** at least. Works perfectly on higher versions.  
> **jquery.dataTables v1.10.8** or higher version.
> **[jquery.dataTables.select extension](https://github.com/DataTables/Select)**


**Features**

- Drag & drop onto table row to select a range of rows.
- Hold Ctrl to add item to an existing selection.
  
**Usages**

```html
	<!-- reference both css and js files -->
    <script src="js/jquery.dataTables.areaselect.js"></script>
    
	<!-- Add a table to your page -->
	<table id="myTable"></table>
 ```
 
```javascript
	// initializes dataTable as usual
	$("#myTable").dataTable({
		data: ...,
		columns: [ ... ],
		select: true, // Activates Select extension
		initComplete: function () {
			// enables area selection extension
			$("#myTable").AreaSelect();
		}
	});
```
 
```javascript
	// Select events callback
	$("#myTable").DataTable()
		.on("select", function (e, dt, type, indexes) {
			if (type === "row") {
		        	var data = $("#myTable").DataTable().rows(indexes).data()[0];
		        	console.info("select", data);
		    	}
		})
		.on("deselect", function (e, dt, type, indexes) {
			if (type === "row") {
				var data = $("#myTable").DataTable().rows(indexes).data();
				console.info("deselect", data);
			}
		});
```

## License

Released under the [MIT license](http://www.opensource.org/licenses/MIT).
