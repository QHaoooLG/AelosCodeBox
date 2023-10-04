Blockly.Blocks['1632297591698'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297591698",
      "message0": "boxLeft",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297591698'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(100,100,100,65,100,100,100,65,100,100,100,65,100,100,100,65,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 101, 100, 93, 55, 124, 100, 100, 15, 99, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(20,20,20,85,85,95,85,85,20,20,20,85,100,100,100,85,0,0,0)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 101, 90, 98, 64, 122, 90, 100, 15, 99, 95, 107, 146, 76, 95, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 101, 95, 93, 54, 124, 90, 100, 15, 99, 105, 107, 146, 76, 100, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(12)\nMOTOmove19(100, 185, 101, 98, 93, 54, 124, 102, 100, 15, 99, 109, 107, 146, 76, 112, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(9)\nMOTOmove19(100, 185, 101, 98, 94, 54, 124, 102, 100, 15, 99, 103, 105, 139, 81, 109, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(9)\nMOTOmove19(100, 185, 101, 98, 93, 54, 124, 102, 100, 15, 99, 103, 105, 139, 81, 109, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 101, 100, 93, 55, 124, 100, 100, 15, 99, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\n";
  return code;
}

