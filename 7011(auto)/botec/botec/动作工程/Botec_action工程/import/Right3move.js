Blockly.Blocks['1632297739358'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297739358",
      "message0": "Right3move",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297739358'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(20,20,20,70,85,95,85,70,20,20,20,70,85,95,85,70,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(80, 35, 100, 90, 93, 54, 123, 100, 120, 155, 100, 110, 107, 146, 76, 110, 128, 71, 0)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(25)\nMOTOmove19(80, 45, 100, 86, 93, 54, 124, 78, 120, 165, 100, 106, 107, 146, 76, 97, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(23)\nMOTOmove19(80, 45, 100, 97, 103, 74, 114, 87, 120, 165, 100, 104, 107, 146, 78, 96, 128, 71, 0)\nMOTOwait()\nDelayMs(50)\nMOTOrigid16(40,40,40,100,100,100,100,100,40,40,40,100,100,100,100,100,0,0,0)\nMOTOsetspeed(18)\nMOTOmove19(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 0)\nMOTOwait()\n";
  return code;
}

