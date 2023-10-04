Blockly.Blocks['Right_flank_kick'] = {
  init: function () {
    this.jsonInit({
      type: "Right_flank_kick",
      message0: "%{BKY_RIGHT_FLANK_KICK}",
      previousStatement: null,
      nextStatement: null,
      colour: "#7148F5",
      toolip: "",
      helpUrl: ""
    });
  }
};

Blockly.Lua['Right_flank_kick'] = function (block) {
  const code = [
    "MOTOrigid16(25,25,25,70,70,70,70,70,25,25,25,70,70,70,70,70)",
    "MOTOsetspeed(15)",
    "MOTOmove16(80, 30, 100, 103, 93, 55, 124, 103, 120, 170, 100, 103, 107, 145, 76, 103)",
    "MOTOwait()",
    "MOTOmove16(80, 40, 100, 105, 93, 54, 124, 105, 120, 160, 100, 110, 109, 152, 71, 112)",
    "MOTOwait()",
    "MOTOmove16(80, 40, 100, 105, 93, 54, 124, 110, 120, 160, 100, 110, 109, 152, 71, 112)",
    "MOTOwait()",
    "MOTOsetspeed(65)",
    "MOTOmove16(80, 60, 100, 105, 93, 55, 124, 114, 120, 140, 100, 140, 95, 115, 95, 120)",
    "MOTOwait()",
    "DelayMs(50)",
    "MOTOsetspeed(36)",
    "MOTOmove16(80, 35, 100, 104, 93, 54, 124, 100, 120, 165, 100, 110, 109, 152, 71, 112)",
    "MOTOwait()",
    "MOTOsetspeed(12)",
    "MOTOmove16(80, 30, 100, 100, 93, 55, 124, 98, 120, 170, 100, 100, 107, 145, 76, 102)",
    "MOTOwait()",
    ""
  ];
  return code.join("\n");
}

