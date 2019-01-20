var str="<p>Hello World!</p>";
var array=[];
document.write(str);
console.log(str);

function buildArray(numRows,numColumns) {
  // handle no values
  if (numRows==0) {
    console.log("No rows.");
    return
  }
  if (numColumns==0) {
    console.log("No columns.");
      return
  }
  // build the actual array
  for (; numRows>0; numRows--) {
    var tmpColumns=numColumns;
    var colArray=[];

    for (; tmpColumns>0; tmpColumns--) {
      colArray.push("@");
    }
    array.push(colArray);
  }
  return array
}

// display the board
function displayBoard(array) {
  var numRows=array.length-1;
  var numColumns=array[numRows].length-1;
  for (; numRows>=0; numRows--) {
    var row="<p class='board'>";
    var tmpColumns=numColumns;
    while (tmpColumns>=0) {
      row += "|"
      row += array[numRows][tmpColumns];
      tmpColumns--;
    }

    row += "</p>";
    console.log(row);
    document.write(row);
  }
}

// valid number
function validNumber(row, column) {
  var numRows=array.length;
  var numColumns=array[numRows-1].length;
  if (row>numRows){
    return "The row specified is not on the board.";
  }
  if (column>numColumns) {
    return "The column specified is not on the board.";
  }
  if (row|column>1) {
    return "Please enter a value greater than 0."
  }
}

buildArray(3,3);
displayBoard(array);
