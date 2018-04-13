/**
 * Responds to any HTTP request that provides the below JSON message in the body.
 * # Example input JSON : {"number1": 1, "operand": "mul", "number2": 2 }
 * @param {!Object} req Cloud Function request context.
 * @param {!Object} res Cloud Function response context.
 */
exports.calculator = function calculator(req, res) {
  
  if (req.body.operand === undefined) {
    res.status(400).send('No operand defined!');
  } else {
    // Everything is okay
    console.log("Received number1",req.body.number1);
    console.log("Received operand",req.body.operand);
    console.log("Received number2",req.body.number2);

    var error, result;
    
    if (isNaN(req.body.number1) || isNaN(req.body.number2)) {
        console.error("Invalid Numbers");			// different logging
        error = "Invalid Numbers!";
        res.status(400).send(error);

    }

    switch(req.body.operand)
    {
        case "+":
        case "add":
            result = req.body.number1 + req.body.number2;
            break;
        case "-":
        case "sub":
            result = req.body.number1 - req.body.number2;
            break;
        case "*":
        case "mul":
            result = req.body.number1 * req.body.number2;
            break;
        case "/":
        case "div":
            if(req.body.number2 === 0){
            	console.error("The divisor cannot be 0");
                error = "The divisor cannot be 0";
                res.status(400).send(error);
            }
            else{
                result = req.body.number1/req.body.number2;
            }
            break;
        default:
            res.status(400).send("Invalid operand");
            break;
    }
    console.log("The Result is: " + result);

    res.status(200).send('The result is: ' + result);
  }
};

