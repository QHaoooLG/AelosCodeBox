Blockly.Blocks['1632297634423'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297634423",
      "message0": "boxTurnR2",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297634423'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(30,30,30,100,65,65,65,65,30,30,30,100,65,65,65,65,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 101, 95, 113, 55, 144, 95, 100, 15, 99, 105, 127, 145, 96, 105, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 101, 95, 121, 55, 144, 92, 100, 15, 99, 105, 128, 145, 96, 108, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 101, 100, 93, 55, 124, 100, 100, 15, 99, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\nDelayMs(400)\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 101, 100, 93, 55, 124, 100, 100, 15, 99, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\n";
  return code;
}

