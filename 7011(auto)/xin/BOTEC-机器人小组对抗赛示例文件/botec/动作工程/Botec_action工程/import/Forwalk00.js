Blockly.Blocks['1632297654894'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297654894",
      "message0": "Forwalk00",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297654894'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(40,40,40,80,85,95,85,80,40,40,40,80,85,95,85,80,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(80, 30, 100, 97, 93, 55, 124, 98, 120, 170, 100, 100, 107, 146, 76, 98, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(25)\nMOTOmove19(80, 30, 100, 96, 105, 55, 138, 97, 120, 170, 100, 100, 107, 147, 78, 96, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(12)\nMOTOmove19(80, 30, 100, 96, 98, 55, 128, 106, 120, 170, 100, 100, 110, 147, 86, 106, 128, 71, 0)\nMOTOwait()\nDelayMs(50)\nMOTOsetspeed(12)\nMOTOmove19(80, 30, 100, 100, 93, 55, 124, 104, 120, 170, 100, 100, 102, 139, 81, 105, 128, 71, 0)\nMOTOwait()\nDelayMs(50)\nMOTOrigid16(40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,0,0,0)\nMOTOsetspeed(5)\nMOTOmove19(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 0)\nMOTOwait()\n";
  return code;
}

