Blockly.Blocks['1632297627867'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297627867",
      "message0": "boxTurnL2",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297627867'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(30,30,30,100,65,65,65,65,30,30,30,100,65,65,65,65,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 101, 95, 73, 55, 104, 95, 100, 15, 99, 105, 87, 145, 56, 105, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 101, 95, 72, 55, 104, 92, 100, 15, 99, 105, 79, 145, 56, 108, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 101, 100, 93, 55, 124, 100, 100, 15, 99, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\nDelayMs(400)\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 101, 100, 93, 55, 124, 100, 100, 15, 99, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\n";
  return code;
}

