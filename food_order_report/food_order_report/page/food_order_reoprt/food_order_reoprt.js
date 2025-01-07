frappe.pages['food-order-reoprt'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Food Order Reoprt',
		single_column: true
	});
	controller = new frappe.food_order_report(wrapper);
}

frappe.food_order_report = Class.extend({
	init : function(wrapper){
		var me = this;
		me.wrapper_page = wrapper.page
		this.page = $(wrapper).find('.layout-main-section-wrapper');
		$(frappe.render_template('food_order_reoprt_html')).appendTo(this.page);
		me.id=0
		var showData="true";
		me.base_data()
		me.month()
	},
	base_data:function(){
		var me= this;
		var data
		frappe.call({
			method: "food_order_report.food_order_report.page.food_order_reoprt.food_order_reoprt.fetch_food_orders",
			async: false,
			freeze_message:"Loading ...Please Wait",
			args:{
				'month': me.month_no
			},
			callback: function(r) {
				if(r.message){
					data=r.message
				}
			}
		})
		me.display_table(data)


	},
	display_table:function(data){
		var me= this;
		$('.orders').html($(frappe.render_template('food_order_reoprt_table',{"data":data})));
	},
	month:function(){
		var me= this;
		var month = frappe.ui.form.make_control({
			 parent: this.page.find(".month"),
			 df: {
				 label: '',
				 fieldtype: "Select",
				 options: ["1","2","3","4","5","6","7","8","9","10","11","12"],
				 fieldname: "",
				 placeholder: __(""),
				 default: 1,
				 change:function(){
					 $("#month").val(month.get_value())
					 me.month_no=month.get_value()
					 me.base_data()
			 }
		 },
		 only_input: false,
	 });
	 month.refresh();
 },

	
})
