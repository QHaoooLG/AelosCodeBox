Blockly.Blocks['1632297598375'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297598375",
      "message0": "boxRight",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297598375'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(100,100,100,65,100,100,100,65,100,100,100,65,100,100,100,65,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 101, 100, 93, 55, 124, 100, 100, 15, 99, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(20,20,20,85,100,100,100,85,20,20,20,85,85,95,85,85,0,0,0)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 101, 105, 93, 54, 124, 105, 100, 15, 99, 110, 102, 136, 78, 110, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 101, 94, 93, 54, 124, 100, 100, 15, 99, 106, 107, 146, 76, 110, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(12)\nMOTOmove19(100, 185, 101, 91, 93, 54, 124, 88, 100, 15, 99, 102, 107, 146, 76, 98, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(9)\nMOTOmove19(100, 185, 101, 97, 95, 61, 119, 91, 100, 15, 99, 102, 107, 146, 76, 98, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(9)\nMOTOmove19(100, 185, 101, 97, 95, 61, 119, 91, 100, 15, 99, 102, 107, 146, 76, 98, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 101, 100, 93, 55, 124, 100, 100, 15, 99, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\n";
  return code;
}

