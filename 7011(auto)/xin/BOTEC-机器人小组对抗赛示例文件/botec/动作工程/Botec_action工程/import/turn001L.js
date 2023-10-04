Blockly.Blocks['1632297751472'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297751472",
      "message0": "turn001L",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297751472'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(30,30,30,85,85,85,85,45,30,30,30,85,85,85,85,45,0,0,0)\nMOTOsetspeed(60)\nMOTOmove19(80, 30, 85, 103, 96, 55, 130, 103, 120, 170, 85, 101, 110, 145, 82, 103, 128, 71, 0)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(6)\nMOTOmove19(80, 35, 100, 104, 93, 54, 124, 108, 120, 165, 100, 110, 109, 152, 71, 112, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(6)\nMOTOmove19(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 0)\nMOTOwait()\nDelayMs(300)\n";
  return code;
}

