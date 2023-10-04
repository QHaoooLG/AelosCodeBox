Blockly.Blocks['1632297784847'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297784847",
      "message0": "turn004L",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297784847'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(40,40,40,60,80,80,80,60,40,40,40,60,80,80,80,60,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(80, 30, 100, 100, 93, 55, 124, 94, 120, 170, 100, 100, 107, 145, 76, 95, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(30)\nMOTOmove19(80, 30, 115, 95, 77, 55, 104, 92, 120, 170, 115, 105, 83, 145, 56, 108, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(20)\nMOTOmove19(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 0)\nMOTOwait()\nDelayMs(300)\n";
  return code;
}

