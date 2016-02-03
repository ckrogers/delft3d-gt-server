"use strict";var UI=function(e){void 0===e&&console.error("No models argument for UI"),this.models=e,this.validateForm()};UI.prototype.getModels=function(){return this.models},UI.prototype.UpdateModelList=function(e){var t=this;if(void 0===e||$.isArray(e)!==!0)return void console.log("not an array");var o=$("#list-model-status tbody"),r="",n=0;$.each(e,function(e,t){var o=t.fields;r+="<tr id='model-"+o.uuid+"' class='"+o.status+"'>",r+="<td>"+o.name+"</td>",r+="<td>"+o.status+" "+o.progress+"%</td>",r+="<td>"+o.timeleft+"</td>",r+="<td class='column-actions'><button class='btn btn-border btn-small btn-model-delete' data-uuid='"+o.uuid+"'><span class='glyphicon glyphicon-remove' ></span></button></td>",r+="</tr>",n++}),o.empty(),o.html(r),o.find(".btn-model-delete").click(function(){var e=$(this).data("uuid");t.getModels().deleteModel({uuid:e},function(){$("#model-"+e).remove()})})},UI.prototype.registerHandlers=function(){var e=this;$("#newrun-submit").click(function(){var t={},o={};t.runid=$("#newrun-name").val(),t.author="placeholder",o.timestep=$("#newrun-timestep").val(),e.models.prepareModel(t,o,function(t){void 0!==t&&void 0!==t.status&&("error"===t.status.code&&($("#newrun-alert .alert").html("An error occured! Reason:"+t.status.reason),$("#newrun-alert .alert").removeClass("alert-success").addClass("alert-warning"),$("#newrun-alert").show()),"success"===t.status.code&&($("#newrun-alert .alert").html("Model is starting..."),$("#newrun-alert .alert").removeClass("alert-warning").addClass("alert-success"),$("#newrun-alert").show(),e.models.runModel(t.uuid)),e.models.getModels($.proxy(e.UpdateModelList,e)))})}),$("#run-model-input-properties input").on("change keyup",function(){e.validateForm()})},UI.prototype.validateForm=function(){function e(e){var t=$("#newrun-submit");e===!0?t.removeAttr("disabled"):t.attr("disabled","disabled")}for(var t=new InputValidation,o=[{id:"#newrun-timestep",method:t.ValidateNumberRange},{id:"#newrun-name",method:t.ValidateAsciiString}],r=!0,n=0;n<o.length;n++){var a=o[n],i=$(a.id),d=a.method(i,i.val());d===!1&&(r=!1);var s=i.closest(".input-group");s.toggleClass("error",!d),e(r)}},"undefined"!=typeof module&&module.exports&&(module.exports=UI);var Models=function(){console.log(this)};Models.prototype.setConfiguration=function(e){this.BaseURL=e.BaseURL},Models.prototype.MochaTest=function(e,t){return e+t},Models.prototype.toggleAutoUIRefresh=function(e,t){function o(){-1!==r.refreshTimerId&&(clearInterval(r.refreshTimerId),r.refreshTimerId=-1)}var r=this;t>0?(o(),console.log("Start timer"),r.refreshTimerId=setInterval(function(){r.getModels(e)},t)):o()},Models.prototype.getModels=function(e){var t=this;$.ajax({url:t.BaseURL+"/runs/"}).done(function(t){$("#alert-connectionfailed").hide(),void 0!==e&&e(t)}).error(function(){$("#alert-connectionfailed").show()})},Models.prototype.prepareModel=function(e,t,o){var r=this;console.log("test");var n={type:"startrun",name:e.runid,dt:t.timestep};return console.log(r),$.ajax({url:r.BaseURL+"/createrun/",data:n,method:"GET"}).done(function(e){void 0!==o&&o(e)}),!0},Models.prototype.runModel=function(e,t){var o=this;if(void 0!==e){var r={uuid:e};$.ajax({url:o.BaseURL+"/dorun/",data:r,method:"GET",done:function(e){void 0!==t&&t(e)}})}},Models.prototype.deleteModel=function(e,t){var o=this;if(void 0===e)return!1;if(void 0===e.uuid||0===e.uuid.length)return!1;var r={type:"deleterun"};r.parameters={},r.uuid=e.uuid,$.ajax({url:o.BaseURL+"/deleterun/",data:r,method:"GET"}).done(function(e){void 0!==t&&t(e)})},"undefined"!=typeof module&&module.exports&&(module.exports=Models);var InputValidation=function(){};InputValidation.prototype.ValidateNumberRange=function(e,t){var o,r=e.attr("min"),n=e.attr("max");return void 0===r&&(r=0),void 0===n&&(n=0),r>=n&&console.error("Max is <= min"),0!==n&&(o={min:0,max:n}),validator.isInt(t,o)},InputValidation.prototype.ValidateAsciiString=function(e,t){var o=validator.isAscii(t),r=e.attr("maxlength");return void 0!==r&&(o=o&&validator.isLength(t,{min:0,max:r})),o},"undefined"!=typeof module&&module.exports&&(module.exports=InputValidation),function(){var e={BaseURL:"http://10.0.1.2:8000"},t=new Models;t.setConfiguration(e);var o=new UI(t);o.registerHandlers(),t.getModels(o.UpdateModelList),t.toggleAutoUIRefresh($.proxy(o.UpdateModelList,o),2e4)}();