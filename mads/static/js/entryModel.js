$(document).ready(function () {
  var counter = 0;
  var entryList = {};
  var catList = "";

  $('body').ready(function(){
    $('#newEntry').trigger('click');
  });

  category_list.forEach(cat => {
    catList += `<option value="${cat['id']}">${cat['name']}</option>`;
  });


  $('#newEntry').click(function(){
    var entryForm = `<div class="col-lg-3 col-sm-5 col-12 shadow py-3 mx-lg-4 mx-sm-2 my-3 rounded bg-primary" id="entry${++counter}">
                      <div class="form-group">     
                      <div class="px-3 row">
                        <label class="col-form-label text-white my-auto">Entry ${counter}</label>
                        <svg width="16" height="16" fill="#ffffff" class="bi bi-dash-circle-fill align-middle ml-auto remove-form" viewBox="0 0 16 16" id="entry${counter}">
                          <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7z"/>
                        </svg>
                      </div>
                      <input class="form-control mt-2 entryInput" type="text" id="title${counter}" name="title${counter}" placeholder="Enter title ..." autocomplete="off">
                      </div>
                      <div class="row">
                      <div class="form-group col-lg-5 col-sm-12 col-12">   
                        <select class="form-control" name="category${counter}">
                        ${catList}
                        </select>
                      </div>
                      <div class="form-group col-lg-7 col-sm-12 col-12"> 
                        <select class="form-control" name="status${counter}">
                            <option>Plan to Watch</option>
                            <option>Watching</option>
                            <option>Completed</option>
                            <option>Dropped</option>
                        </select>
                      </div>
                      </div>
                      <div class="form-group form-inline">
                        <label class="col-form-label text-white">Episode</label>
                        <input class="col-8 form-control ml-auto" type="number" id="episode${counter}" name="episode${counter}" value="0" min="0" step="0.5">
                      </div>
                      <div class="form-group form-inline">
                        <label class="col-form-label text-white">Favourite</label>
                        <select class="col-8 form-control ml-auto" name="favourite${counter}">
                            <option>No comment</option>
                            <option>Favourite</option>
                        </select>
                      </div>
                    </div>`;
    $("#entryList").append(entryForm);
    entryList['entry'+counter] = 'title'+counter;
    $("#submitBtn").prop("disabled", true);
  });

  $(document).on('click', '.remove-form', function(){
    var id = this.id;
    $('#'+id).remove();
    delete entryList[id];
    $('.entryInput').trigger('keyup');
  });

  $(document).on('keyup', '.entryInput', () => {
    var counter = 0;
    var len = 0;

    $.each(entryList, (key, val) => {
      len++;
      if ($("#"+val).val())
        counter++;
    });
    
    $("#submitBtn").prop("disabled", () => {
      if (len == counter) return false;
      else return true;
    });
  });
});
