// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Master Sales Order Template', {
	refresh: function(frm) {
		
		frappe.require([
			"assets/erpnext/js/salesTemplatetable.js",
			"assets/erpnext/css/myTable.css",
		]);
		$( "div[data-fieldname*='usd']" ).css('display','none');
		
		$('.indicator').css('display','none');
		$( "button[data-fieldname*='save_order']" ).removeClass( "btn-default" ).addClass( "btn-primary" );
		$( "button[data-fieldname*='save_order']" ).css('padding','8px');

		$( "button[data-fieldname*='update_order']" ).removeClass( "btn-default" ).addClass( "btn-primary" );
		$( "button[data-fieldname*='update_order']" ).css('padding','8px');
		$.ajax({
			url: '/api/resource/Master Sales Order/' + frm.doc.mso_id,
			type: 'get',
			dataType: "json",
			success: function( data ) {
				//console.log(data.data);
				if(data.data.master_sales_order_item.length > 0) 
				{
					var TableArray = [];
					TableArray.push({'name':frm.doc.name});
					var ItemArray = [];
					ItemArray.push({'name':frm.doc.name});
					//console.log(data.data.master_sales_order_item.length);
					for (var i = 0; i < data.data.master_sales_order_item.length; i++) 
					{
						var dta = data.data.master_sales_order_item[i];
						var gw = dta.gross_weight;
						if(isNaN(gw)) { gw = 0; }
						var itmcd = { 'item_name': dta.item_name , 'row_number': dta.row_number, 'item_code': dta.item_code, 'weight': dta.weight, 'weight_per_unit': dta.weight_per_unit,  'uom': dta.uom,  'ppk_calculation': dta.ppk_calculation,  'gross_weight': gw, 'description': dta.description, 'purchase_pallets': dta.purchase_pallets, 'col_number': "0", isuppliers: [] };		
						if(dta.address_title) { var address_title = dta.address_title; } else { var address_title = ""; }		
						if(dta.address) { var address = dta.address; } else { var address = ""; }
						if(dta.po_no) { var po_no = dta.po_no; } else { var po_no = ""; }
						if(dta.mso_notes) { var mso_notes = dta.mso_notes; } else { var mso_notes = ""; }
						//if(frm.doc.template_mso) {  dta.qty = 0; dta.received_qty = 0; dta.price = 0;  }
						var splcd = {'name': dta.name, 'qty': dta.qty, 'received_qty': dta.received_qty, 'price': dta.price, 'customer_name': dta.customer_name, 'customer': dta.customer , 'default_currency': dta.default_currency  , 'default_price_list': dta.default_price_list , 'mso_notes': mso_notes , 'po_no': po_no  , 'address_title': address_title , 'address': address , 'col_number' : dta.col_number};
				
				 
						if( ItemArray.length > 1 ) 
						{
							if(typeof ItemArray[dta.row_number] != "undefined") {
					 TableArray[dta.row_number].push(splcd);
						}
						else {
ItemArray[dta.row_number] = [];							
ItemArray[dta.row_number].push(itmcd);
							itmcd.isuppliers.push(splcd);
TableArray[dta.row_number] = []; 						
TableArray[dta.row_number].push(itmcd);
						TableArray[dta.row_number].push(splcd);
							}
						}
						else {
ItemArray[dta.row_number] = [];	
						ItemArray[dta.row_number].push(itmcd);
						TableArray[dta.row_number] = []; 						
						TableArray[dta.row_number].push(itmcd);
						TableArray[dta.row_number].push(splcd);
						}
		
					}	
					
				}
//console.log(ItemArray); 
//console.log(TableArray);
				var show_x = "";
				if(frm.doc.status == "Draft") { show_x = "X"; 
				$( "button[data-fieldname*='add_column']" ).css('display','block');
					$( "button[data-fieldname*='add_row']" ).css('display','block');
					}
				
				
				
				var table = '<tr data-row="0"><td data-row="0" data-col="0"></td><td data-row="0" data-col="1"> </td><td data-row="0" data-col="2"></td><td data-row="0" data-col="3"></td>'; 
				var dataCol = 4;
				var dataCol1 = dataCol;
				var t1 = '<tr data-row="1"><td data-row="1" data-col="0"></td><td data-row="1" data-col="1"> </td><td data-row="1" data-col="2"></td><td data-row="1" data-col="3"></td>'; 
				var t2 = '<tr data-row="2"><td data-row="2" data-col="0"></td><td data-row="2" data-col="1">Items</td><td data-row="2" data-col="2">Item Name</td><td data-row="2" data-col="3">Lbs/Box</td>';
				var titems = '';
				var dataRow = 3; var spcol = 0; var ttlcol = 1; var colStart = 4;
				var tlCols = ''; //alert(TableArray.length);
				for(var v=1; v < TableArray.length; v++) {
					
					TableArray[v].sort(function(obj1, obj2) {
						return obj1.col_number - obj2.col_number;
					});
					
			titems = titems + '<tr class="item-row" data-row="'+dataRow +'"><td data-row="'+dataRow +'" data-col="0"><a href="javascript:;" class="del" onClick="salesTemplatetable_DelRow('+dataRow +')">'+show_x+'</a></td><td data-row="'+dataRow +'" data-col="1"><div class="autocomplete"><input type="hidden" class="uom" name="uom" value="' +TableArray[v][0].uom + '"><input type="hidden" class="sitemsid" name="sitemsid" value="' +TableArray[v][0].item_code + '"><input type="hidden" class="item_code" name="item_code" value="' +TableArray[v][0].item_code + '"><input type="hidden" class="ppk_calculation" name="ppk_calculation" value="' +TableArray[v][0].ppk_calculation + '"><input type="text" class="sitems" id="sitems'+dataRow +'" name="sitems" value="' +TableArray[v][0].item_code + '"></div></td><td data-row="'+dataRow +'" data-col="2"><input type="text" name="idesc" disabled="disabled" class="idesc" value="' +TableArray[v][0].description+ '"></td><td data-row="'+dataRow +'" data-col="3"><input type="hidden" class="purchase_pallets"  name="purchase_pallets" value="' +TableArray[v][0].purchase_pallets+ '"><input type="hidden" class="gross_weight"  name="gross_weight" value="' +TableArray[v][0].gross_weight+ '"><input type="text" class="weight" name="weight" value="' +TableArray[v][0].weight_per_unit+ '"></td>';	
			
			for(var k=1; k < TableArray[v].length; k++)
			{
				if(spcol == 0 )
				{
				
				var dpl="STD";
				if(TableArray[1][k].default_price_list != "undefined" && TableArray[1][k].default_price_list && TableArray[1][k].default_price_list != null) { dpl = TableArray[1][k].default_price_list; }
				
				t1 = t1 + '<td data-row="1" data-col="'+ dataCol1 +'"><input type="hidden" class="isupplierid" name="isupplierid" value="'+ TableArray[1][k].customer +'"><input type="hidden" class="default_currency" name="default_currency" value="'+ TableArray[1][k].default_currency +'"><input type="hidden" class="default_price_list" name="default_price_list" value="'+ dpl +'"><input type="hidden" class="address" name="address" value="'+ TableArray[1][k].address +'"><input type="text" class="mso_notes" placeholder="MSO notes/Comments" name="mso_notes" value="'+ TableArray[1][k].mso_notes +'"><div class="autocomplete"><input type="text" id="isupplier'+ dataCol1 +'" class="isupplier"  name="isupplier'+ dataCol1 +'" value="'+ TableArray[1][k].customer +'"></div><input type="text" placeholder="PO number"  class="po_no" name="po_no" value="'+ TableArray[1][k].po_no +'"><div class="autocomplete"><input type="text" id="address_title'+ dataCol1 +'" placeholder="Customer Address"  class="address_title" name="address_title'+ dataCol1 +'" value="'+ TableArray[1][k].address_title +'"></div></td>';

table = table + '<td data-row="0" data-col="'+dataCol1 +'"><a href="javascript:;" class="delCol" onClick="salesTemplatetable_DelCol('+ dataCol1 +')">'+show_x+'</a></td>';
					
					t2 = t2 + '<td data-row="2" data-col="'+ dataCol1 +'"><div class="text-span">Qty </div><div class="text-span"> Price</div></td>';
				}
				titems = titems  + '<td data-row="'+ dataRow +'" data-col="' + dataCol1 + '"><input type="hidden" class="iname' + dataCol1 + '" id="iname" name="iname' + dataCol1 + '" value="'+ TableArray[v][k].name +'"><input type="hidden" class="rqty' + dataCol1 + '" id="rqty" name="rqty' + dataCol1 + '" value="'+ TableArray[v][k].received_qty +'"><input type="text" class="iqty' + dataCol1 + '" id="iqty" name="iqty' + dataCol1 + '" value="'+ TableArray[v][k].qty +'"><input type="text" name="iprice' + dataCol1 + '" class="iprice' + dataCol1 + '" value="'+ TableArray[v][k].price +'"  id="iprice"></td>';
						
				if(spcol == 0) {
	tlCols = tlCols + '<td data-row="'+ (TableArray.length + 2) +'" data-col="'+ dataCol1 +'"><p id="qtotal" class="qtotal'+ dataCol1 +'">0</p><p id="stotal" class="stotal'+ dataCol1 +'">0.0</p></td>';		ttlcol  = colStart + k;
				}
			dataCol1 = dataCol1 + 1;			
					//console.log(TableArray[v][k]);
				} spcol = spcol + 1;
					titems = titems  + '<td data-row="'+dataRow +'" data-col="'+dataCol1+'"><span class="qtytotal">0.0</span></td><td data-row="'+dataRow +'" data-col="'+(dataCol1 + 1)+'"><span class="ppktotal">0.0</span></td></tr>';
		
		dataCol1 = 4;
		dataCol  = dataCol + 1;	
		dataRow = dataRow + 1;		
				}
				table  = table + ' <td data-row="0" data-col="'+ttlcol +'"> <td data-row="0" data-col="'+ (ttlcol + 1) +'"></tr>';
				
t1 = t1 + '<td data-row="1" data-col="'+ttlcol +'"><td data-row="1" data-col="'+ (ttlcol + 1) +'"></tr>'
;
t2 = t2 + '<td data-row="2" data-col="'+ttlcol +'" class="width60">Boxes</td><td data-row="2" data-col="'+ (ttlcol +1) +'" class="width60">Bulk Boxes</td></tr>';
				table = table  + t1;
				table = table + t2;
				table = table + titems;
table = table + '<tr class="item-row" data-row="'+dataRow+'"><td data-row="'+dataRow+'" data-col="0"></td><td data-row="'+dataRow+'" data-col="1"></td><td data-row="'+dataRow+'" data-col="2"></td><td data-row="'+dataRow+'" data-col="3"></td>'+tlCols+'<td data-row="'+dataRow+'" data-col="'+ ttlcol + '"><span class="qtytotal_total"></span></td><td data-row="'+dataRow+'" data-col="'+ (ttlcol+1) + '"><span class="ppktotal_total"></span></td></tr>';
				
				var $wrapper = $("div[data-fieldname='customeritemstpl']").empty();
	$wrapper.html('<div style="overflow-x:auto;"><table id="salesTemplatetable"  border="1" class="display nowrap dataTable dtr-inline">'+table+'</table><script type="text/javascript">$("#salesTemplatetable").on("click", ".isupplier", function() { var idd = $(this).attr("id"); autocompletesupplier2(idd); }); $("#salesTemplatetable").on("click", ".address_title", function() { var idd = $(this).attr("id"); autocompleteaddress2(idd); }); $("#salesTemplatetable").on("change", "input", function() { $(this).updatedata1(); }); $("#salesTemplatetable").on("click", ".sitems", function() { var row = $(this).parents(".item-row"); var idd = row.find(".sitems").attr("id"); autocomplete2(idd); }); $("#salesTemplatetable").find(".sitems").each( function(){ $(this).updatedata1(); });</script></div>');
				//$('#salesTemplatetable').html(table);
				
				$("#salesTemplatetable").find(".sitems").each( function(){ 
					$(this).updatedata1();
				});
				
				if(frm.doc.status == "Saved") {
					$("#salesTemplatetable input").prop("disabled", true);
					$( "button[data-fieldname*='add_column']" ).css('display','none');
					$( "button[data-fieldname*='add_row']" ).css('display','none');
				}
				
			}
			});

		
			frm.add_custom_button(__("Save Draft"), function() {
					//console.log(frm.doc);
					var shd = '';
					var MasterArray = [];
					var MasterPOItems = { 'shipping_date': frm.doc.shipping_date, 'delivery_date': frm.doc.delivery_date, 'cad': frm.doc.cad,  'usd': frm.doc.usd,  'pallet_weight': frm.doc.pallet_weight, 'total_boxes': '0', 'total_pallets': '0', 'total_weight': '0', 'total_actual_cost': 0, 'total_actual_cost_usd': 0,'name':frm.doc.name, 'master_sales_order_item' : [] };

					MasterArray.push({
						'name':frm.doc.name,
						'shipping_date': frm.doc.shipping_date,    
						'delivery_date': frm.doc.delivery_date,    
						'cad': frm.doc.cad,  
						'usd': frm.doc.usd,
						'total_boxes': '0',
						'total_pallets': '0',
						'total_weight': '0',
						'total_actual_cost': 0,
						'total_actual_cost_usd': 0
					});
					var ItemsArray = [];
					var vindex = 0;
					var col_number = 0; var validate_items = "";
					$("#salesTemplatetable").find(".sitems").each( function()
					{
						var row = $(this).parents('.item-row');
						if(row.find('.sitems').val() != '' && row.find('.item_code').val() == '') 
						{
							validate_items = validate_items + "#" +row.find('.sitems').attr('id') + ", ";
						}
						if(row.find('.item_code').val() != '') 
						{
							var salesTemplatetable = $('#salesTemplatetable');
							var colCount = salesTemplatetable.find('td[data-row=0]').length;
							shd = shd + row.find('.sitems').val();
							shd = shd + 'Description: ' + row.find('.idesc').val();
							
							vindex = vindex+1;
							var arrr = 'array'+vindex;
							MasterArray[arrr] = [];
							var weight = parseFloat(row.find('.weight').val());
							var purchase_pallets = parseFloat(row.find('.purchase_pallets').val());
							var gross_weight = parseFloat(row.find('.gross_weight').val());
								
							if(isNaN(weight)) { row.find('.weight').val(0);  }
							if(isNaN(purchase_pallets)) { row.find('.purchase_pallets').val(0.0); }
							if(isNaN(gross_weight)) { row.find('.gross_weight').val(0.0); }
							
							var itmcd = {'item_code': row.find('.item_code').val(), 'weight': weight, 'purchase_pallets': purchase_pallets, 'gross_weight': gross_weight};
							MasterArray[arrr].push(itmcd);		
							
							var total_boxes = 0; 
							var total_pallet = 0;
							var total_net_weight = 0;
							var total_gross_weight_lbs = 0;
							var total_weight_kg = 0;
							
							for(var i = 4; i < (colCount -2); i++) 
							{
								var sidcell = $("#isupplier"+i).parents('td');
								if($('#isupplier'+i).val() != '' && sidcell.find('.isupplierid').val() == '') 
								{
									validate_items = validate_items + "#isupplier"+i + ", ";
								}
								if($('#isupplier'+i).val() != '')
								{
								var mso_notes =  sidcell.find('.mso_notes').val();
								var po_no =  sidcell.find('.po_no').val();
								var address =  sidcell.find('.address').val();
								var address_title =  $('#address_title'+i).val();	
								col_number  = col_number + 1;
								var iqty = parseFloat(row.find('.iqty'+i).val());
								var iprice = parseFloat(row.find('.iprice'+i).val());
								
								if(isNaN(iqty)) { row.find('.iqty'+i).val(0);  }
								if(isNaN(iprice)) { row.find('.iprice'+i).val(0.0); }
								
								shd = shd + ' Suplier'+i+': ' + $('#isupplier'+i).val();
								shd = shd + ' Qty'+i+': ' + iqty;
								shd = shd +  ' Price'+i+': ' + iprice;
								
								
								var qty = $('.iqty' + i);
								var price = $('.iprice' + i);

								for (var k = 0; k < qty.length; k++) {
									total_boxes = total_boxes + parseFloat(qty[k].value);
									if(row.find('.purchase_pallets').val() > 0) 
									{
										total_pallet = total_pallet + (parseFloat(qty[k].value) / parseFloat(row.find('.purchase_pallets').val()));
									}
									total_net_weight = total_net_weight + parseFloat(qty[k].value * row.find('.weight').val());
									total_gross_weight_lbs = total_gross_weight_lbs +  parseFloat(qty[k].value * row.find('.gross_weight').val());
									total_weight_kg = total_weight_kg +  parseFloat(total_gross_weight_lbs * 0.45359237);
								}
								
								var itmsp = {'customer': $('#isupplier'+i).val(),'qty': iqty,'rate': iprice};
									MasterArray[arrr].push(itmsp);	
								var listitm = {'qty': iqty, 'price': iprice, 'weight': row.find('.weight').val(),  'gross_weight': row.find('.gross_weight').val(),  'uom': row.find('.uom').val(), 'weight_per_unit': row.find('.weight').val(), 'description': row.find('.idesc').val(), 'purchase_pallets': row.find('.purchase_pallets').val(), 'item_code': row.find('.item_code').val(), 'ppk_calculation': row.find('.ppk_calculation').val(), 'item_name': row.find('.idesc').val(),'received_qty' : 0, 'customer_name': $('#isupplier'+i).val(), 'customer': $('#isupplier'+i).val(), 'default_currency': sidcell.find('.default_currency').val(), 'row_number': vindex , 'col_number': col_number, 'total_boxes': total_boxes, 'total_pallet': total_pallet, 'total_net_weight': total_net_weight, 'total_gross_weight_lbs': total_gross_weight_lbs, 'total_weight_kg': total_weight_kg,'mso_notes': mso_notes, 'po_no': po_no, 'address_title': address_title, 'address': address};
								MasterPOItems['master_sales_order_item'].push(listitm);
								
								total_boxes = 0; 
								total_pallet = 0;
								total_net_weight = 0;
								total_gross_weight_lbs = 0;
								total_weight_kg = 0;
								
								}
							}
							col_number = 0;
						}	
					});

				if(validate_items != '') { $(validate_items +' .abc').css('border','1px solid red'); msgprint("Please Select Item and Customer from Dropdown list"); return false; }
				console.log(MasterPOItems);
				var TableArray = [];
									var ItemArray = [];
									for (var i = 0; i < MasterPOItems.master_sales_order_item.length; i++) 
									{
										var dta = MasterPOItems.master_sales_order_item[i];
										var dt_col_num = dta.col_number - 1;
										
										var conversion_rate = 1;
										var plc_conversion_rate = 1;
										if(dta.default_currency == "USD") { 
											if(frm.doc.usd > 0) {
												conversion_rate = parseFloat(1 / frm.doc.usd);
												plc_conversion_rate = parseFloat(1 / frm.doc.usd);
											}
										}
										
										var itmcd1 = { 'customer_name': dta.customer_name, 'customer': dta.customer ,'delivery_date': MasterPOItems.delivery_date ,'shipping_date': MasterPOItems.shipping_date , 'cad': MasterPOItems.cad,  'usd': MasterPOItems.usd, 'conversion_rate': conversion_rate, 'plc_conversion_rate': plc_conversion_rate, 'row_number': dta.row_number, 'col_number':  dta.col_number, 'total_boxes': dta.total_boxes, 'total_pallet': dta.total_pallet, 'total_net_weight': dta.total_net_weight, 'total_gross_weight_lbs': dta.total_gross_weight_lbs, 'total_weight_kg': dta.total_weight_kg,'mso_notes':dta.mso_notes, 'po_no':dta.po_no, 'address_title':dta.address_title, 'address':dta.address, items: [] };				
										var splcd = { 'item_name': dta.description ,  'item_code': dta.item_code, 'ppk_calculation': dta.ppk_calculation, 'weight': dta.weight, 'weight_per_unit': dta.weight_per_unit, 'weight_lbs': dta.weight_per_unit,'gross_weight_lbs': dta.gross_weight, 'description': dta.description, 'purchase_pallets': dta.purchase_pallets, 'boxes_pallet_for_purchase': dta.purchase_pallets, 'qty': dta.qty, 'box': dta.qty, 'uom': dta.uom, 'price': dta.price, 'rate': dta.price, 'schedule_date': MasterPOItems.delivery_date,  'row_number' : dta.row_number,  'col_number' : dta.col_number};
								
								 
										if( ItemArray.length > 0 ) 
										{
											if(typeof ItemArray[dt_col_num] != "undefined") {
												
												TableArray[dt_col_num][0]["items"].push(splcd);
											}
											else {
												ItemArray[dt_col_num] = [];							
												ItemArray[dt_col_num].push(itmcd1);
												TableArray[dt_col_num] = [];
												itmcd1["items"].push(splcd);
												TableArray[dt_col_num].push(itmcd1);
											}
										}
										else {
				ItemArray[dt_col_num] = [];	
										ItemArray[dt_col_num].push(itmcd1);
										TableArray[dt_col_num] = [];
										itmcd1["items"].push(splcd);
										TableArray[dt_col_num].push(itmcd1);
										}
						
									}
				var TableArray1 = {'name': frm.doc.name, 'details': TableArray};
				console.log(TableArray1);
				
				frappe.call({
						method:'erpnext.salesapi.makeMasterPoOrder',
						args: {
							po: MasterPOItems,
							ps: TableArray1
						},
							callback: function(r) {
							console.log(r.message);
							frm.doc.__islocal = 0;
							//window.location.href = "/desk#Form/Master%20Sales%20Order/"+r.message;
							frappe.ui.toolbar.clear_cache();
							frappe.set_route("Form", "Master Sales Order", r.message);
							//location.reload();
						}
					}); 
	
				});

	}
});
