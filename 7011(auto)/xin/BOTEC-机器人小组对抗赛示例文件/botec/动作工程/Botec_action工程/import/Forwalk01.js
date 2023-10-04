Blockly.Blocks['1632297667364'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297667364",
      "message0": "Forwalk01",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297667364'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(40,40,40,40,70,80,70,40,40,40,40,40,70,80,70,40,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(80, 30, 100, 95, 93, 55, 124, 92, 120, 170, 100, 100, 107, 145, 76, 93, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(30)\nMOTOmove19(80, 35, 90, 95, 113, 45, 148, 89, 120, 165, 90, 102, 107, 147, 76, 92, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(13)\nMOTOmove19(80, 35, 90, 99, 96, 54, 126, 107, 120, 165, 90, 104, 125, 146, 94, 108, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(30)\nMOTOmove19(80, 35, 90, 99, 94, 55, 124, 105, 120, 165, 90, 106, 101, 138, 78, 109, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(10)\nMOTOmove19(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 0)\nMOTOwait()\n";
  return code;
}

