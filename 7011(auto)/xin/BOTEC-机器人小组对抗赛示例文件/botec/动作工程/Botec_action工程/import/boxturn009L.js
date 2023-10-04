Blockly.Blocks['1632297609907'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297609907",
      "message0": "boxturn009L",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297609907'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(30,30,30,85,85,85,85,85,30,30,30,85,85,85,85,85,0,0,0)\nMOTOsetspeed(50)\nMOTOmove19(100, 185, 100, 102, 93, 55, 124, 98, 100, 15, 100, 98, 107, 145, 76, 102, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(30,30,30,85,85,85,85,45,30,30,30,85,85,85,85,75,0,0,0)\nMOTOsetspeed(100)\nMOTOmove19(100, 185, 100, 103, 99, 55, 122, 103, 100, 15, 100, 103, 113, 145, 79, 110, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 100, 105, 96, 54, 124, 108, 100, 15, 100, 110, 115, 145, 80, 110, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(30,30,30,30,30,30,30,30,30,30,30,65,75,80,75,65,0,0,0)\n\n\n-- MOTORB,105,62,168,83,95\nMOTOsetspeed(25)\nMOTOmove19(100, 185, 100, 105, 96, 54, 124, 108, 100, 15, 100, 107, 97, 127, 85, 112, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(25)\nMOTOmove19(100, 185, 100, 100, 93, 55, 124, 98, 100, 15, 100, 100, 107, 145, 76, 102, 128, 71, 100)\nMOTOwait()\n";
  return code;
}

