Blockly.Blocks['1632297767228'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297767228",
      "message0": "turn003R",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297767228'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(30,30,30,85,85,85,85,45,30,30,30,85,85,85,85,45,0,0,0)\nMOTOsetspeed(40)\nMOTOmove19(80, 30, 115, 99, 88, 55, 118, 97, 120, 170, 115, 104, 98, 145, 70, 104, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(30)\nMOTOmove19(80, 30, 115, 99, 88, 55, 118, 93, 120, 170, 115, 104, 98, 145, 70, 97, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(30)\nMOTOmove19(80, 30, 100, 100, 98, 65, 119, 96, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(30)\nMOTOmove19(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 0)\nMOTOwait()\n";
  return code;
}

