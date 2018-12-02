frappe.pages['price-list-sheet'].on_page_load = function(wrapper) {
frappe.provide("erpnext");
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Price List Sheet',
		single_column: true
	});
	page.start = 0;
		
	page.item_code = page.add_field({
		fieldname: 'item_code',
		label: __('Item Code'),
		fieldtype:'Link',
		options:'Item',
		change: function() {
				frappe.price_list_sheet.getitem_update(page);

		}
	});
	page.item_group = page.add_field({
		fieldname: 'item_group',
		label: __('Item Group'),
		fieldtype:'Link',
		options:'Item Group',
		change: function() {
				frappe.price_list_sheet.getitem_update(page);

		}
	});
				frappe.price_list_sheet.make(page);
				frappe.price_list_sheet.run(page);
				frappe.price_list_sheet.getitem(page);
				
	
	frappe.require([
	 	"assets/erpnext/css/myTable.css",
		"assets/erpnext/js/pricelistsheet.js",
		"assets/erpnext/js/jquery-ui.js",
	]);
	
	$("#qtyTable").css('cursor','pointer');
	$("#qtyTable").css('overflow','scroll');
	frappe.breadcrumbs.add("Selling")

jQuery.fn.getpopup = function() {
		jsonobj=[]
		filter=[]
		var myTable = document.getElementById("qtyTable");
		console.log(myTable);
		$('#qtyTable1 tr').remove();
		var ths = myTable.getElementsByTagName("th");
		var i;
		for(i=1;i<ths.length;i++)
		{
			price_list={}
			price_list["price_list"]=ths[i].className
			jsonobj.push(price_list)
		}
			
		var data='<h3>Price List</h3><table id="qtyTable1"  border="1" class="display nowrap dataTable dtr-inline" >';
		console.log(jsonobj);
		var k =0;
		$.each(jsonobj, function(idx, obj) {
		
			console.log(obj["pricelist"]);
			data=data+'<tr class="item-row" data-row="'+k+'"><td width="20px" data-row="'+k+'" data-col="0"><a href="javascript:;" class="del" onClick="myTable_DelRow('+k+')">X</a></td><td data-row="'+k+'" data-col="1"><div class="autocomplete"><input onClick="autocomplete1(\'price_list_data'+k+'\')"  autocomplete="off" type="text" class="price_list_data" id="price_list_data'+k+'" name="price_list_data" value="'+obj["price_list"]+'"></div></td></tr>';
			k = k+1;
		});		

		data=data+'</table><button onClick="AddNewRow1()" class="btn-primary" id="addnewRow">Add Row</button><script type="text/javascript">$("#qtyTable1").on("click", ".price_list_data", function() { var row = $(this).parents(".item-row"); var idd = row.find(".price_list_data").attr("id"); autocomplete1(idd); }); var fixHelperModified = function(e, tr) { var $originals = tr.children(); var $helper = tr.clone(); $helper.children().each(function(index) { $(this).width($originals.eq(index).width()) }); return $helper; }, updateIndex = function(e, ui) { $("#qtyTable1 .item-row").each(function (i) { $(this).attr("data-row", i); $(this).find("td").attr("data-row", i); $(this).find(".del").attr("onClick", "myTable_DelRow(\" + i + "\)");  $(this).find(".price_list_data").attr("id", "price_list_data" + i); $(this).find(".price_list_data").attr("onclick", "autocomplete1(\'price_list_data"+ i + "\')");  });}; $("#qtyTable1 tbody").sortable({ helper: fixHelperModified, stop: updateIndex }).disableSelection(); </script>';
		var fields = [
			{fieldtype:'HTML', fieldname: 'price_list'}
			];

					var d = new frappe.ui.Dialog({
						title: __('Select Price List'),
						fields: fields,
						primary_action: function() {
						d.hide();
						var res=document.getElementById("qtyTable1")	
						var res2 = res.getElementsByClassName("price_list_data")
						var arr ={'test':'','items':[]};
						$('.price_list_data').each(function(){

							var list_item={'price_list_name':$(this).val()};
							arr['items'].push(list_item);
						})
						frappe.price_list_sheet.run(page,arr['items']);
						frappe.price_list_sheet.getitem(page);
						console.log("Array:"+arr['items']);
						},
						primary_action_label: __('Update')
					});
				
				d.fields_dict.price_list.$wrapper.html(data);
				d.show();
				d.$wrapper.find('.modal-dialog').css("width", "1000px");





}
	
jQuery.fn.getpopup1 = function() {
		
		var tdclass = $(this).attr('class'); // onclick any td will give you that td "class" attribute value  that we will use for th "id"	
		
		var th_price_list_name = $("#"+tdclass).html();
		//alert(th_price_list_name);
		
		var row = $(this).parents('.itm-row');
		var td_item_code = row.find(".td_item_code").html();
		//alert(td_item_code);
		
		console.log($(this)[0].innerHTML.replace('<br>',''));
		console.log($("#"+tdclass).html());
		if($(this)[0].innerHTML.replace('<br>','')>0){
		frappe.call({
							method:"erpnext.price_list_sheet.updatePriceListValue",
							args:{'item_code':row.find(".td_item_code").html(),'price_list_name':$("#"+tdclass).html(),'rate':$(this)[0].innerHTML.replace('<br>','')},
							callback:function(r){
									console.log("call");

								if(r.message){
									msg='Price Update For '+row.find(".td_item_code").html()+' In Price List '+$("#"+tdclass).html()
				
									show_alert(msg,4);
									}
								//setTimeout(function(){
										// frappe.price_list_sheet.getitem_update(page)},500)
								}
								
						})
			}
		
		/* var fields1 = [
			{fieldtype:'Data', fieldname:'rate'}
			];

					var d = new frappe.ui.Dialog({
						title: __('Update Rate'),
						fields: fields1,
						primary_action: function() {
						d.hide();
						frappe.call({
							method:"erpnext.price_list_sheet.updatePriceListValue",
							args:{'item_code':row.find(".td_item_code").html(),'price_list_name':$("#"+tdclass).html(),'rate':d.get_values().rate},
							callback:function(r){
								setTimeout(function(){console.log("call");
										 frappe.price_list_sheet.getitem_update(page)},500)
								}
								
						})
						console.log(d.get_values().rate)
						},
						primary_action_label: __('Update')
					});
					console.log($(this)[0].innerHTML)
					d.set_value('rate',$(this)[0].innerHTML)
					d.show(); */



};		

}

frappe.price_list_sheet= {
	start: 0,
	make: function(page) {
		var me = frappe.price_list_sheet;
		me.page = page;
		me.body=$('<button style="float:right" class="btn-primary" id="price_list_add">Add PriceList</button><script type="text/javascript"> $("#price_list_add").on("click",function(){ $(this).getpopup(); }); </script>').appendTo(me.page.main);	
		$("#qtyTable").remove();
		//alert();
		
	
	},
	run: function(page,obj) {
		var me = frappe.price_list_sheet;
		me.page=page;
		console.log("call");
		$(".frstmn").hide();

		$("#qtyTable").remove();

		if(obj===undefined)
		{
		frappe.call({
			'method': 'erpnext.price_list_sheet.getColumn',
			'args':{date:'test'},
			'freeze': true,
			'freeze_message': "Please Wait...",
			callback: function(r) {
			if(r.message) {
			console.log(r.message)
			me.body=$('<table id="qtyTable"  border="1" class="display nowrap dataTable dtr-inline" width="100%"></table><script type="text/javascript">$("#qtyTable").css("cursor","pointer"); $("#qtyTable").on("blur","td",function(){ $(this).getpopup1(); });</script>').appendTo(me.page.main);

					var data='<tr class="item_column"><th id="item_code" class="item_code">Item Code</th>'
					r.message.forEach(function(d,index) {
						data=data+'<th class="'+d.name+'" id="td_price_list_name'+(index+2)+'">'+d.name+'</th>'
					
					});
					data=data+'</tr>'
					$("#qtyTable").append(data);
		
				}
			
				
			
			}
		});
		}
		else
		{
			me.body=$('<table id="qtyTable"  border="1" class="display nowrap dataTable dtr-inline" width="100%"></table><script type="text/javascript">$("#qtyTable").css("cursor","pointer");$(".first").click(function(){alert("Test");	}); $("#qtyTable").on("blur","td",function(){ $(this).getpopup1(); });</script>').appendTo(me.page.main);

					var data='<tr class="item_column"><th id="item_code" class="item_code">Item Code</th>'
					console.log(obj)
					plist_arr=[]
					plist_obj={}
					for(i=0;i<obj.length;i++)
					{
						
						data=data+'<th id="td_price_list_name'+(i+2)+'" class="'+obj[i].price_list_name+'">'+obj[i].price_list_name+'</th>'
						plist_obj["sr_no"]=i;
						plist_obj["name1"]=obj[i].price_list_name;
						plist_arr.push(plist_obj)
						plist_obj={}
					}
					console.log("Plist_arr"+JSON.stringify(plist_arr))
					frappe.call({
							method:"erpnext.price_list_sheet.addPriceList",
							args:{'object_val':plist_arr},
							callback:function(r){
									console.log(r)
						
							}
										
					})
					data=data+'</tr>'
					$("#qtyTable").append(data);
					

	
		}











	},
	getitem:function(page)
	{
		
setTimeout(function(){ 

		jsonobj=[]
		filter=[]
		var myTable = document.getElementById("qtyTable");
		//console.log(myTable);
		var ths = myTable.getElementsByTagName("th");
		//console.log(ths);
		var i;
		for(i=1;i<ths.length;i++)
		{
			price_list={}
			price_list["name"]=ths[i].innerHTML
			jsonobj.push(price_list)
		}
		item={}
		if (typeof page.item_code.value != 'undefined')
		{
			item_code=page.item_code.value
		}
		else{
		
			item_code=null
		}
		if (typeof page.item_group.value != 'undefined')
		{
			item_group=page.item_group.value
		}
		else{
		
			item_group=null
		}
		item["item_code"]=item_code
		item["item_group"]=item_group
		filter.push(item)
		//console.log(item)
		//console.log(jsonobj)
		frappe.call({
			method:"erpnext.price_list_sheet.getData",
			args:{'pricelist_obj':jsonobj,'filters':item},
			freeze: true,
			freeze_message: "Please Wait...",
			callback:function(r){
				//console.log(r.message)
				var count=0;
				var d_row='';
				var end_count=r.message.length
				//console.log("end_count"+end_count);
				for(row in r.message)
				{
					var cnt=0
					var i=0
					var elementid='row'
					var flag=0
					var j = 0
					//console.log('<br />'+row);
					for(row1 in r.message[row])
					{	
						j=j+1
						//console.log(flag)
					//	console.log("row1 - "+[row1])
						if(cnt==0)
						{
						i=i+1
						//$("#qtyTable").append('<tr class="item_row" id=item_row'+i+'></tr>');
						//$(".item_row").append('<td>'+r.message[row][row1]+'</td>')
						//console.log("if")
						var parenttbl = document.getElementById('qtyTable');
						var newel = document.createElement('tr')
						elementid = elementid+document.getElementsByTagName("tr").length
						newel.setAttribute('id',elementid);
						newel.setAttribute('class','itm-row');						
//console.log("eid:"+elementid);
						//newel.innerHTML = r.message[row][row1]
						parenttbl.appendChild(newel);
						var parenttbl = document.getElementById(elementid);
						var newel = document.createElement('td')
						var elementid1 = document.getElementsByTagName("td").length
						newel.setAttribute('id',elementid1);
						newel.setAttribute('class','td_item_code')
						newel.innerHTML = r.message[row]['item']
						parenttbl.appendChild(newel)
						cnt=cnt+1
					
						}
						else{
				
						if(flag>=1)
						{
	
							//console.log("flag")

							continue;
							
						}
						else{
							for(price in jsonobj)
							{
							//var row_val='r.message[row].price'+i.toString();
							//console.log(row_val)
							//d_row=d_row+'<td>'+row_val+'</td>'

									//console.log(jsonobj[price])
									var parenttbl = document.getElementById(elementid);
									var newel = document.createElement('td')
									var elementid1 = document.getElementsByTagName("td").length
									newel.setAttribute('id',elementid1);
									newel.setAttribute('class','td_price_list_name'+j);
									newel.setAttribute('contentEditable','true');
									newel.innerHTML =r.message[row][jsonobj[price].name]
									parenttbl.appendChild(newel);
									cnt=cnt+1;
									flag=flag+1
									j=j+1
							

						

							}
						}
						}
						
					}
					//$(".item_row").append(d_row);				
				}
				
				/*$.each(r.message, function(idx, obj) {
					console.log(idx)
					if(idx==0)
					{
					$("#qtyTable").append('<tr class="item_row"></tr>');
					$(".item_row").append('<td>'+obj["item"]+'</td>')
					}
					else{
				d_row=d_row+'<td>'+obj["price"+count]+'</td>'
					}
			
				
				})
					$(".item_row").append(d_row);*/
				
				
				
			}
					
		})

 }, 1500);

		
			
	},
	getitem_update:function(page)
	{
		
setTimeout(function(){ 
		//console.log("getitem");
		jsonobj=[]
		filter=[]
        	 var rowCount = qtyTable.rows.length;
       		 for (var j = rowCount - 1; j > 0; j--) {
       			     qtyTable.deleteRow(j);
        		}
		var myTable = document.getElementById("qtyTable");
		//console.log(myTable);
		var ths = myTable.getElementsByTagName("th");
		//console.log(ths);
		var i;
		for(i=1;i<ths.length;i++)
		{
			price_list={}
			price_list["name"]=ths[i].innerHTML
			jsonobj.push(price_list)
		}
		item={}
		if (typeof page.item_code.value != 'undefined')
		{
			item_code=page.item_code.value
		}
		else{
		
			item_code=null
		}
		if (typeof page.item_group.value != 'undefined')
		{
			item_group=page.item_group.value
		}
		else{
		
			item_group=null
		}
		item["item_code"]=item_code
		item["item_group"]=item_group
		filter.push(item)
		//console.log(item)
		//console.log(jsonobj)
		frappe.call({
			method:"erpnext.price_list_sheet.getData",
			args:{'pricelist_obj':jsonobj,'filters':item},
			freeze: true,
			freeze_message: "Please Wait...",
			callback:function(r){
				//console.log(r.message)
				var count=0;
				var d_row='';
				var end_count=r.message.length
				//console.log("end_count"+end_count);
				for(row in r.message)
				{
					var cnt=0
					var i=0
					var elementid='row'
					var flag=0
					var j = 0
					//console.log('<br />'+row);
					for(row1 in r.message[row])
					{	
						j=j+1
						//console.log(flag)
					//	console.log("row1 - "+[row1])
						if(cnt==0)
						{
						i=i+1
						//$("#qtyTable").append('<tr class="item_row" id=item_row'+i+'></tr>');
						//$(".item_row").append('<td>'+r.message[row][row1]+'</td>')
						//console.log("if")
						var parenttbl = document.getElementById('qtyTable');
						var newel = document.createElement('tr')
						elementid = elementid+document.getElementsByTagName("tr").length
						newel.setAttribute('id',elementid);
						newel.setAttribute('class','itm-row');						
//console.log("eid:"+elementid);
						//newel.innerHTML = r.message[row][row1]
						parenttbl.appendChild(newel);
						var parenttbl = document.getElementById(elementid);
						var newel = document.createElement('td')
						var elementid1 = document.getElementsByTagName("td").length
						newel.setAttribute('id',elementid1);
						newel.setAttribute('class','td_item_code')
						newel.innerHTML = r.message[row]['item']
						parenttbl.appendChild(newel)
						cnt=cnt+1
					
						}
						else{
				
						if(flag>=1)
						{
	
							//console.log("flag")

							continue;
							
						}
						else{
							for(price in jsonobj)
							{
							//var row_val='r.message[row].price'+i.toString();
							//console.log(row_val)
							//d_row=d_row+'<td>'+row_val+'</td>'

									//console.log(jsonobj[price])
									var parenttbl = document.getElementById(elementid);
									var newel = document.createElement('td')
									var elementid1 = document.getElementsByTagName("td").length
									newel.setAttribute('id',elementid1);
									newel.setAttribute('class','td_price_list_name'+j);
									newel.setAttribute('contentEditable','true');
									newel.innerHTML =r.message[row][jsonobj[price].name]
									parenttbl.appendChild(newel);
									cnt=cnt+1;
									flag=flag+1
									j=j+1
							

						

							}
						}
						}
						
					}
					//$(".item_row").append(d_row);				
				}
				
				/*$.each(r.message, function(idx, obj) {
					console.log(idx)
					if(idx==0)
					{
					$("#qtyTable").append('<tr class="item_row"></tr>');
					$(".item_row").append('<td>'+obj["item"]+'</td>')
					}
					else{
				d_row=d_row+'<td>'+obj["price"+count]+'</td>'
					}
			
				
				})
					$(".item_row").append(d_row);*/
				
				
				
			}
					
		})

 },1500);

		
			
	}
		
}
