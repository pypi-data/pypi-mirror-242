const {
  SvelteComponent: kt,
  assign: yt,
  create_slot: vt,
  detach: Ct,
  element: qt,
  get_all_dirty_from_scope: Ft,
  get_slot_changes: Lt,
  get_spread_update: Mt,
  init: St,
  insert: zt,
  safe_not_equal: Vt,
  set_dynamic_element_data: ze,
  set_style: S,
  toggle_class: E,
  transition_in: ot,
  transition_out: rt,
  update_slot_base: Nt
} = window.__gradio__svelte__internal;
function At(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[17].default
  ), f = vt(
    i,
    n,
    /*$$scope*/
    n[16],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-1t38q2d"
    }
  ], o = {};
  for (let r = 0; r < s.length; r += 1)
    o = yt(o, s[r]);
  return {
    c() {
      e = qt(
        /*tag*/
        n[14]
      ), f && f.c(), ze(
        /*tag*/
        n[14]
      )(e, o), E(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), E(
        e,
        "padded",
        /*padding*/
        n[6]
      ), E(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), E(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), S(e, "height", typeof /*height*/
      n[0] == "number" ? (
        /*height*/
        n[0] + "px"
      ) : void 0), S(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : void 0), S(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), S(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), S(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), S(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), S(e, "border-width", "var(--block-border-width)");
    },
    m(r, a) {
      zt(r, e, a), f && f.m(e, null), l = !0;
    },
    p(r, a) {
      f && f.p && (!l || a & /*$$scope*/
      65536) && Nt(
        f,
        i,
        r,
        /*$$scope*/
        r[16],
        l ? Lt(
          i,
          /*$$scope*/
          r[16],
          a,
          null
        ) : Ft(
          /*$$scope*/
          r[16]
        ),
        null
      ), ze(
        /*tag*/
        r[14]
      )(e, o = Mt(s, [
        (!l || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          r[7]
        ) },
        (!l || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          r[2]
        ) },
        (!l || a & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        r[3].join(" ") + " svelte-1t38q2d")) && { class: t }
      ])), E(
        e,
        "hidden",
        /*visible*/
        r[10] === !1
      ), E(
        e,
        "padded",
        /*padding*/
        r[6]
      ), E(
        e,
        "border_focus",
        /*border_mode*/
        r[5] === "focus"
      ), E(e, "hide-container", !/*explicit_call*/
      r[8] && !/*container*/
      r[9]), a & /*height*/
      1 && S(e, "height", typeof /*height*/
      r[0] == "number" ? (
        /*height*/
        r[0] + "px"
      ) : void 0), a & /*width*/
      2 && S(e, "width", typeof /*width*/
      r[1] == "number" ? `calc(min(${/*width*/
      r[1]}px, 100%))` : void 0), a & /*variant*/
      16 && S(
        e,
        "border-style",
        /*variant*/
        r[4]
      ), a & /*allow_overflow*/
      2048 && S(
        e,
        "overflow",
        /*allow_overflow*/
        r[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && S(
        e,
        "flex-grow",
        /*scale*/
        r[12]
      ), a & /*min_width*/
      8192 && S(e, "min-width", `calc(min(${/*min_width*/
      r[13]}px, 100%))`);
    },
    i(r) {
      l || (ot(f, r), l = !0);
    },
    o(r) {
      rt(f, r), l = !1;
    },
    d(r) {
      r && Ct(e), f && f.d(r);
    }
  };
}
function Bt(n) {
  let e, t = (
    /*tag*/
    n[14] && At(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(l, i) {
      t && t.m(l, i), e = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && t.p(l, i);
    },
    i(l) {
      e || (ot(t, l), e = !0);
    },
    o(l) {
      rt(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function It(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: s = void 0 } = e, { elem_id: o = "" } = e, { elem_classes: r = [] } = e, { variant: a = "solid" } = e, { border_mode: _ = "base" } = e, { padding: u = !0 } = e, { type: c = "normal" } = e, { test_id: m = void 0 } = e, { explicit_call: h = !1 } = e, { container: L = !0 } = e, { visible: q = !0 } = e, { allow_overflow: M = !0 } = e, { scale: g = null } = e, { min_width: d = 0 } = e, C = c === "fieldset" ? "fieldset" : "div";
  return n.$$set = (w) => {
    "height" in w && t(0, f = w.height), "width" in w && t(1, s = w.width), "elem_id" in w && t(2, o = w.elem_id), "elem_classes" in w && t(3, r = w.elem_classes), "variant" in w && t(4, a = w.variant), "border_mode" in w && t(5, _ = w.border_mode), "padding" in w && t(6, u = w.padding), "type" in w && t(15, c = w.type), "test_id" in w && t(7, m = w.test_id), "explicit_call" in w && t(8, h = w.explicit_call), "container" in w && t(9, L = w.container), "visible" in w && t(10, q = w.visible), "allow_overflow" in w && t(11, M = w.allow_overflow), "scale" in w && t(12, g = w.scale), "min_width" in w && t(13, d = w.min_width), "$$scope" in w && t(16, i = w.$$scope);
  }, [
    f,
    s,
    o,
    r,
    a,
    _,
    u,
    m,
    h,
    L,
    q,
    M,
    g,
    d,
    C,
    c,
    i,
    l
  ];
}
class Pt extends kt {
  constructor(e) {
    super(), St(this, e, It, Bt, Vt, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 15,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: Zt,
  append: he,
  attr: re,
  create_component: Tt,
  destroy_component: jt,
  detach: Et,
  element: Ve,
  init: Dt,
  insert: Rt,
  mount_component: Ht,
  safe_not_equal: Yt,
  set_data: Ut,
  space: Xt,
  text: Gt,
  toggle_class: D,
  transition_in: Ot,
  transition_out: Jt
} = window.__gradio__svelte__internal;
function Kt(n) {
  let e, t, l, i, f, s;
  return l = new /*Icon*/
  n[1]({}), {
    c() {
      e = Ve("label"), t = Ve("span"), Tt(l.$$.fragment), i = Xt(), f = Gt(
        /*label*/
        n[0]
      ), re(t, "class", "svelte-9gxdi0"), re(e, "for", ""), re(e, "data-testid", "block-label"), re(e, "class", "svelte-9gxdi0"), D(e, "hide", !/*show_label*/
      n[2]), D(e, "sr-only", !/*show_label*/
      n[2]), D(
        e,
        "float",
        /*float*/
        n[4]
      ), D(
        e,
        "hide-label",
        /*disable*/
        n[3]
      );
    },
    m(o, r) {
      Rt(o, e, r), he(e, t), Ht(l, t, null), he(e, i), he(e, f), s = !0;
    },
    p(o, [r]) {
      (!s || r & /*label*/
      1) && Ut(
        f,
        /*label*/
        o[0]
      ), (!s || r & /*show_label*/
      4) && D(e, "hide", !/*show_label*/
      o[2]), (!s || r & /*show_label*/
      4) && D(e, "sr-only", !/*show_label*/
      o[2]), (!s || r & /*float*/
      16) && D(
        e,
        "float",
        /*float*/
        o[4]
      ), (!s || r & /*disable*/
      8) && D(
        e,
        "hide-label",
        /*disable*/
        o[3]
      );
    },
    i(o) {
      s || (Ot(l.$$.fragment, o), s = !0);
    },
    o(o) {
      Jt(l.$$.fragment, o), s = !1;
    },
    d(o) {
      o && Et(e), jt(l);
    }
  };
}
function Qt(n, e, t) {
  let { label: l = null } = e, { Icon: i } = e, { show_label: f = !0 } = e, { disable: s = !1 } = e, { float: o = !0 } = e;
  return n.$$set = (r) => {
    "label" in r && t(0, l = r.label), "Icon" in r && t(1, i = r.Icon), "show_label" in r && t(2, f = r.show_label), "disable" in r && t(3, s = r.disable), "float" in r && t(4, o = r.float);
  }, [l, i, f, s, o];
}
class Wt extends Zt {
  constructor(e) {
    super(), Dt(this, e, Qt, Kt, Yt, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: xt,
  append: $t,
  attr: we,
  binding_callbacks: el,
  create_slot: tl,
  detach: ll,
  element: Ne,
  get_all_dirty_from_scope: nl,
  get_slot_changes: il,
  init: fl,
  insert: sl,
  safe_not_equal: ol,
  toggle_class: R,
  transition_in: rl,
  transition_out: al,
  update_slot_base: _l
} = window.__gradio__svelte__internal;
function cl(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[5].default
  ), f = tl(
    i,
    n,
    /*$$scope*/
    n[4],
    null
  );
  return {
    c() {
      e = Ne("div"), t = Ne("div"), f && f.c(), we(t, "class", "icon svelte-3w3rth"), we(e, "class", "empty svelte-3w3rth"), we(e, "aria-label", "Empty value"), R(
        e,
        "small",
        /*size*/
        n[0] === "small"
      ), R(
        e,
        "large",
        /*size*/
        n[0] === "large"
      ), R(
        e,
        "unpadded_box",
        /*unpadded_box*/
        n[1]
      ), R(
        e,
        "small_parent",
        /*parent_height*/
        n[3]
      );
    },
    m(s, o) {
      sl(s, e, o), $t(e, t), f && f.m(t, null), n[6](e), l = !0;
    },
    p(s, [o]) {
      f && f.p && (!l || o & /*$$scope*/
      16) && _l(
        f,
        i,
        s,
        /*$$scope*/
        s[4],
        l ? il(
          i,
          /*$$scope*/
          s[4],
          o,
          null
        ) : nl(
          /*$$scope*/
          s[4]
        ),
        null
      ), (!l || o & /*size*/
      1) && R(
        e,
        "small",
        /*size*/
        s[0] === "small"
      ), (!l || o & /*size*/
      1) && R(
        e,
        "large",
        /*size*/
        s[0] === "large"
      ), (!l || o & /*unpadded_box*/
      2) && R(
        e,
        "unpadded_box",
        /*unpadded_box*/
        s[1]
      ), (!l || o & /*parent_height*/
      8) && R(
        e,
        "small_parent",
        /*parent_height*/
        s[3]
      );
    },
    i(s) {
      l || (rl(f, s), l = !0);
    },
    o(s) {
      al(f, s), l = !1;
    },
    d(s) {
      s && ll(e), f && f.d(s), n[6](null);
    }
  };
}
function ul(n) {
  let e, t = n[0], l = 1;
  for (; l < n.length; ) {
    const i = n[l], f = n[l + 1];
    if (l += 2, (i === "optionalAccess" || i === "optionalCall") && t == null)
      return;
    i === "access" || i === "optionalAccess" ? (e = t, t = f(t)) : (i === "call" || i === "optionalCall") && (t = f((...s) => t.call(e, ...s)), e = void 0);
  }
  return t;
}
function dl(n, e, t) {
  let l, { $$slots: i = {}, $$scope: f } = e, { size: s = "small" } = e, { unpadded_box: o = !1 } = e, r;
  function a(u) {
    if (!u)
      return !1;
    const { height: c } = u.getBoundingClientRect(), { height: m } = ul([
      u,
      "access",
      (h) => h.parentElement,
      "optionalAccess",
      (h) => h.getBoundingClientRect,
      "call",
      (h) => h()
    ]) || { height: c };
    return c > m + 2;
  }
  function _(u) {
    el[u ? "unshift" : "push"](() => {
      r = u, t(2, r);
    });
  }
  return n.$$set = (u) => {
    "size" in u && t(0, s = u.size), "unpadded_box" in u && t(1, o = u.unpadded_box), "$$scope" in u && t(4, f = u.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*el*/
    4 && t(3, l = a(r));
  }, [s, o, r, l, f, i, _];
}
class ml extends xt {
  constructor(e) {
    super(), fl(this, e, dl, cl, ol, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: bl,
  append: J,
  attr: v,
  detach: gl,
  init: hl,
  insert: wl,
  noop: pe,
  safe_not_equal: pl,
  svg_element: X
} = window.__gradio__svelte__internal;
function kl(n) {
  let e, t, l, i, f, s, o;
  return {
    c() {
      e = X("svg"), t = X("circle"), l = X("circle"), i = X("circle"), f = X("circle"), s = X("circle"), o = X("path"), v(t, "cx", "20"), v(t, "cy", "4"), v(t, "r", "2"), v(t, "fill", "currentColor"), v(l, "cx", "8"), v(l, "cy", "16"), v(l, "r", "2"), v(l, "fill", "currentColor"), v(i, "cx", "28"), v(i, "cy", "12"), v(i, "r", "2"), v(i, "fill", "currentColor"), v(f, "cx", "11"), v(f, "cy", "7"), v(f, "r", "2"), v(f, "fill", "currentColor"), v(s, "cx", "16"), v(s, "cy", "24"), v(s, "r", "2"), v(s, "fill", "currentColor"), v(o, "fill", "currentColor"), v(o, "d", "M30 3.413L28.586 2L4 26.585V2H2v26a2 2 0 0 0 2 2h26v-2H5.413Z"), v(e, "xmlns", "http://www.w3.org/2000/svg"), v(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), v(e, "aria-hidden", "true"), v(e, "role", "img"), v(e, "class", "iconify iconify--carbon"), v(e, "width", "100%"), v(e, "height", "100%"), v(e, "preserveAspectRatio", "xMidYMid meet"), v(e, "viewBox", "0 0 32 32");
    },
    m(r, a) {
      wl(r, e, a), J(e, t), J(e, l), J(e, i), J(e, f), J(e, s), J(e, o);
    },
    p: pe,
    i: pe,
    o: pe,
    d(r) {
      r && gl(e);
    }
  };
}
class at extends bl {
  constructor(e) {
    super(), hl(this, e, null, kl, pl, {});
  }
}
const yl = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Ae = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
yl.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: Ae[e][t],
      secondary: Ae[e][l]
    }
  }),
  {}
);
function Q(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function ce() {
}
function vl(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const _t = typeof window < "u";
let Be = _t ? () => window.performance.now() : () => Date.now(), ct = _t ? (n) => requestAnimationFrame(n) : ce;
const W = /* @__PURE__ */ new Set();
function ut(n) {
  W.forEach((e) => {
    e.c(n) || (W.delete(e), e.f());
  }), W.size !== 0 && ct(ut);
}
function Cl(n) {
  let e;
  return W.size === 0 && ct(ut), {
    promise: new Promise((t) => {
      W.add(e = { c: n, f: t });
    }),
    abort() {
      W.delete(e);
    }
  };
}
const K = [];
function ql(n, e = ce) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(o) {
    if (vl(n, o) && (n = o, t)) {
      const r = !K.length;
      for (const a of l)
        a[1](), K.push(a, n);
      if (r) {
        for (let a = 0; a < K.length; a += 2)
          K[a][0](K[a + 1]);
        K.length = 0;
      }
    }
  }
  function f(o) {
    i(o(n));
  }
  function s(o, r = ce) {
    const a = [o, r];
    return l.add(a), l.size === 1 && (t = e(i, f) || ce), o(n), () => {
      l.delete(a), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: s };
}
function Ie(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function ve(n, e, t, l) {
  if (typeof t == "number" || Ie(t)) {
    const i = l - t, f = (t - e) / (n.dt || 1 / 60), s = n.opts.stiffness * i, o = n.opts.damping * f, r = (s - o) * n.inv_mass, a = (f + r) * n.dt;
    return Math.abs(a) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, Ie(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => ve(n, e[f], t[f], l[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = ve(n, e[f], t[f], l[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Pe(n, e = {}) {
  const t = ql(n), { stiffness: l = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let s, o, r, a = n, _ = n, u = 1, c = 0, m = !1;
  function h(q, M = {}) {
    _ = q;
    const g = r = {};
    return n == null || M.hard || L.stiffness >= 1 && L.damping >= 1 ? (m = !0, s = Be(), a = q, t.set(n = _), Promise.resolve()) : (M.soft && (c = 1 / ((M.soft === !0 ? 0.5 : +M.soft) * 60), u = 0), o || (s = Be(), m = !1, o = Cl((d) => {
      if (m)
        return m = !1, o = null, !1;
      u = Math.min(u + c, 1);
      const C = {
        inv_mass: u,
        opts: L,
        settled: !0,
        dt: (d - s) * 60 / 1e3
      }, w = ve(C, a, n, _);
      return s = d, a = n, t.set(n = w), C.settled && (o = null), !C.settled;
    })), new Promise((d) => {
      o.promise.then(() => {
        g === r && d();
      });
    }));
  }
  const L = {
    set: h,
    update: (q, M) => h(q(_, n), M),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: f
  };
  return L;
}
const {
  SvelteComponent: Fl,
  append: N,
  attr: y,
  component_subscribe: Ze,
  detach: Ll,
  element: Ml,
  init: Sl,
  insert: zl,
  noop: Te,
  safe_not_equal: Vl,
  set_style: ae,
  svg_element: A,
  toggle_class: je
} = window.__gradio__svelte__internal, { onMount: Nl } = window.__gradio__svelte__internal;
function Al(n) {
  let e, t, l, i, f, s, o, r, a, _, u, c;
  return {
    c() {
      e = Ml("div"), t = A("svg"), l = A("g"), i = A("path"), f = A("path"), s = A("path"), o = A("path"), r = A("g"), a = A("path"), _ = A("path"), u = A("path"), c = A("path"), y(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), y(i, "fill", "#FF7C00"), y(i, "fill-opacity", "0.4"), y(i, "class", "svelte-43sxxs"), y(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), y(f, "fill", "#FF7C00"), y(f, "class", "svelte-43sxxs"), y(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), y(s, "fill", "#FF7C00"), y(s, "fill-opacity", "0.4"), y(s, "class", "svelte-43sxxs"), y(o, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), y(o, "fill", "#FF7C00"), y(o, "class", "svelte-43sxxs"), ae(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), y(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), y(a, "fill", "#FF7C00"), y(a, "fill-opacity", "0.4"), y(a, "class", "svelte-43sxxs"), y(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), y(_, "fill", "#FF7C00"), y(_, "class", "svelte-43sxxs"), y(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), y(u, "fill", "#FF7C00"), y(u, "fill-opacity", "0.4"), y(u, "class", "svelte-43sxxs"), y(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), y(c, "fill", "#FF7C00"), y(c, "class", "svelte-43sxxs"), ae(r, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), y(t, "viewBox", "-1200 -1200 3000 3000"), y(t, "fill", "none"), y(t, "xmlns", "http://www.w3.org/2000/svg"), y(t, "class", "svelte-43sxxs"), y(e, "class", "svelte-43sxxs"), je(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(m, h) {
      zl(m, e, h), N(e, t), N(t, l), N(l, i), N(l, f), N(l, s), N(l, o), N(t, r), N(r, a), N(r, _), N(r, u), N(r, c);
    },
    p(m, [h]) {
      h & /*$top*/
      2 && ae(l, "transform", "translate(" + /*$top*/
      m[1][0] + "px, " + /*$top*/
      m[1][1] + "px)"), h & /*$bottom*/
      4 && ae(r, "transform", "translate(" + /*$bottom*/
      m[2][0] + "px, " + /*$bottom*/
      m[2][1] + "px)"), h & /*margin*/
      1 && je(
        e,
        "margin",
        /*margin*/
        m[0]
      );
    },
    i: Te,
    o: Te,
    d(m) {
      m && Ll(e);
    }
  };
}
function Bl(n, e, t) {
  let l, i, { margin: f = !0 } = e;
  const s = Pe([0, 0]);
  Ze(n, s, (c) => t(1, l = c));
  const o = Pe([0, 0]);
  Ze(n, o, (c) => t(2, i = c));
  let r;
  async function a() {
    await Promise.all([s.set([125, 140]), o.set([-125, -140])]), await Promise.all([s.set([-125, 140]), o.set([125, -140])]), await Promise.all([s.set([-125, 0]), o.set([125, -0])]), await Promise.all([s.set([125, 0]), o.set([-125, 0])]);
  }
  async function _() {
    await a(), r || _();
  }
  async function u() {
    await Promise.all([s.set([125, 0]), o.set([-125, 0])]), _();
  }
  return Nl(() => (u(), () => r = !0)), n.$$set = (c) => {
    "margin" in c && t(0, f = c.margin);
  }, [f, l, i, s, o];
}
class Il extends Fl {
  constructor(e) {
    super(), Sl(this, e, Bl, Al, Vl, { margin: 0 });
  }
}
const {
  SvelteComponent: Pl,
  append: O,
  attr: I,
  binding_callbacks: Ee,
  check_outros: dt,
  create_component: Zl,
  create_slot: Tl,
  destroy_component: jl,
  destroy_each: mt,
  detach: p,
  element: T,
  empty: ee,
  ensure_array_like: me,
  get_all_dirty_from_scope: El,
  get_slot_changes: Dl,
  group_outros: bt,
  init: Rl,
  insert: k,
  mount_component: Hl,
  noop: Ce,
  safe_not_equal: Yl,
  set_data: V,
  set_style: H,
  space: P,
  text: F,
  toggle_class: z,
  transition_in: x,
  transition_out: $,
  update_slot_base: Ul
} = window.__gradio__svelte__internal, { tick: Xl } = window.__gradio__svelte__internal, { onDestroy: Gl } = window.__gradio__svelte__internal, Ol = (n) => ({}), De = (n) => ({});
function Re(n, e, t) {
  const l = n.slice();
  return l[38] = e[t], l[40] = t, l;
}
function He(n, e, t) {
  const l = n.slice();
  return l[38] = e[t], l;
}
function Jl(n) {
  let e, t = (
    /*i18n*/
    n[1]("common.error") + ""
  ), l, i, f;
  const s = (
    /*#slots*/
    n[29].error
  ), o = Tl(
    s,
    n,
    /*$$scope*/
    n[28],
    De
  );
  return {
    c() {
      e = T("span"), l = F(t), i = P(), o && o.c(), I(e, "class", "error svelte-14miwb5");
    },
    m(r, a) {
      k(r, e, a), O(e, l), k(r, i, a), o && o.m(r, a), f = !0;
    },
    p(r, a) {
      (!f || a[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      r[1]("common.error") + "") && V(l, t), o && o.p && (!f || a[0] & /*$$scope*/
      268435456) && Ul(
        o,
        s,
        r,
        /*$$scope*/
        r[28],
        f ? Dl(
          s,
          /*$$scope*/
          r[28],
          a,
          Ol
        ) : El(
          /*$$scope*/
          r[28]
        ),
        De
      );
    },
    i(r) {
      f || (x(o, r), f = !0);
    },
    o(r) {
      $(o, r), f = !1;
    },
    d(r) {
      r && (p(e), p(i)), o && o.d(r);
    }
  };
}
function Kl(n) {
  let e, t, l, i, f, s, o, r, a, _ = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Ye(n)
  );
  function u(d, C) {
    if (
      /*progress*/
      d[7]
    )
      return xl;
    if (
      /*queue_position*/
      d[2] !== null && /*queue_size*/
      d[3] !== void 0 && /*queue_position*/
      d[2] >= 0
    )
      return Wl;
    if (
      /*queue_position*/
      d[2] === 0
    )
      return Ql;
  }
  let c = u(n), m = c && c(n), h = (
    /*timer*/
    n[5] && Ge(n)
  );
  const L = [ln, tn], q = [];
  function M(d, C) {
    return (
      /*last_progress_level*/
      d[15] != null ? 0 : (
        /*show_progress*/
        d[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = M(n)) && (s = q[f] = L[f](n));
  let g = !/*timer*/
  n[5] && $e(n);
  return {
    c() {
      _ && _.c(), e = P(), t = T("div"), m && m.c(), l = P(), h && h.c(), i = P(), s && s.c(), o = P(), g && g.c(), r = ee(), I(t, "class", "progress-text svelte-14miwb5"), z(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), z(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(d, C) {
      _ && _.m(d, C), k(d, e, C), k(d, t, C), m && m.m(t, null), O(t, l), h && h.m(t, null), k(d, i, C), ~f && q[f].m(d, C), k(d, o, C), g && g.m(d, C), k(d, r, C), a = !0;
    },
    p(d, C) {
      /*variant*/
      d[8] === "default" && /*show_eta_bar*/
      d[18] && /*show_progress*/
      d[6] === "full" ? _ ? _.p(d, C) : (_ = Ye(d), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), c === (c = u(d)) && m ? m.p(d, C) : (m && m.d(1), m = c && c(d), m && (m.c(), m.m(t, l))), /*timer*/
      d[5] ? h ? h.p(d, C) : (h = Ge(d), h.c(), h.m(t, null)) : h && (h.d(1), h = null), (!a || C[0] & /*variant*/
      256) && z(
        t,
        "meta-text-center",
        /*variant*/
        d[8] === "center"
      ), (!a || C[0] & /*variant*/
      256) && z(
        t,
        "meta-text",
        /*variant*/
        d[8] === "default"
      );
      let w = f;
      f = M(d), f === w ? ~f && q[f].p(d, C) : (s && (bt(), $(q[w], 1, 1, () => {
        q[w] = null;
      }), dt()), ~f ? (s = q[f], s ? s.p(d, C) : (s = q[f] = L[f](d), s.c()), x(s, 1), s.m(o.parentNode, o)) : s = null), /*timer*/
      d[5] ? g && (g.d(1), g = null) : g ? g.p(d, C) : (g = $e(d), g.c(), g.m(r.parentNode, r));
    },
    i(d) {
      a || (x(s), a = !0);
    },
    o(d) {
      $(s), a = !1;
    },
    d(d) {
      d && (p(e), p(t), p(i), p(o), p(r)), _ && _.d(d), m && m.d(), h && h.d(), ~f && q[f].d(d), g && g.d(d);
    }
  };
}
function Ye(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = T("div"), I(e, "class", "eta-bar svelte-14miwb5"), H(e, "transform", t);
    },
    m(l, i) {
      k(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && H(e, "transform", t);
    },
    d(l) {
      l && p(e);
    }
  };
}
function Ql(n) {
  let e;
  return {
    c() {
      e = F("processing |");
    },
    m(t, l) {
      k(t, e, l);
    },
    p: Ce,
    d(t) {
      t && p(e);
    }
  };
}
function Wl(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, f, s;
  return {
    c() {
      e = F("queue: "), l = F(t), i = F("/"), f = F(
        /*queue_size*/
        n[3]
      ), s = F(" |");
    },
    m(o, r) {
      k(o, e, r), k(o, l, r), k(o, i, r), k(o, f, r), k(o, s, r);
    },
    p(o, r) {
      r[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      o[2] + 1 + "") && V(l, t), r[0] & /*queue_size*/
      8 && V(
        f,
        /*queue_size*/
        o[3]
      );
    },
    d(o) {
      o && (p(e), p(l), p(i), p(f), p(s));
    }
  };
}
function xl(n) {
  let e, t = me(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = Xe(He(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = ee();
    },
    m(i, f) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, f);
      k(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = me(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const o = He(i, t, s);
          l[s] ? l[s].p(o, f) : (l[s] = Xe(o), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && p(e), mt(l, i);
    }
  };
}
function Ue(n) {
  let e, t = (
    /*p*/
    n[38].unit + ""
  ), l, i, f = " ", s;
  function o(_, u) {
    return (
      /*p*/
      _[38].length != null ? en : $l
    );
  }
  let r = o(n), a = r(n);
  return {
    c() {
      a.c(), e = P(), l = F(t), i = F(" | "), s = F(f);
    },
    m(_, u) {
      a.m(_, u), k(_, e, u), k(_, l, u), k(_, i, u), k(_, s, u);
    },
    p(_, u) {
      r === (r = o(_)) && a ? a.p(_, u) : (a.d(1), a = r(_), a && (a.c(), a.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[38].unit + "") && V(l, t);
    },
    d(_) {
      _ && (p(e), p(l), p(i), p(s)), a.d(_);
    }
  };
}
function $l(n) {
  let e = Q(
    /*p*/
    n[38].index || 0
  ) + "", t;
  return {
    c() {
      t = F(e);
    },
    m(l, i) {
      k(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = Q(
        /*p*/
        l[38].index || 0
      ) + "") && V(t, e);
    },
    d(l) {
      l && p(t);
    }
  };
}
function en(n) {
  let e = Q(
    /*p*/
    n[38].index || 0
  ) + "", t, l, i = Q(
    /*p*/
    n[38].length
  ) + "", f;
  return {
    c() {
      t = F(e), l = F("/"), f = F(i);
    },
    m(s, o) {
      k(s, t, o), k(s, l, o), k(s, f, o);
    },
    p(s, o) {
      o[0] & /*progress*/
      128 && e !== (e = Q(
        /*p*/
        s[38].index || 0
      ) + "") && V(t, e), o[0] & /*progress*/
      128 && i !== (i = Q(
        /*p*/
        s[38].length
      ) + "") && V(f, i);
    },
    d(s) {
      s && (p(t), p(l), p(f));
    }
  };
}
function Xe(n) {
  let e, t = (
    /*p*/
    n[38].index != null && Ue(n)
  );
  return {
    c() {
      t && t.c(), e = ee();
    },
    m(l, i) {
      t && t.m(l, i), k(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[38].index != null ? t ? t.p(l, i) : (t = Ue(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && p(e), t && t.d(l);
    }
  };
}
function Ge(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = F(
        /*formatted_timer*/
        n[20]
      ), l = F(t), i = F("s");
    },
    m(f, s) {
      k(f, e, s), k(f, l, s), k(f, i, s);
    },
    p(f, s) {
      s[0] & /*formatted_timer*/
      1048576 && V(
        e,
        /*formatted_timer*/
        f[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && V(l, t);
    },
    d(f) {
      f && (p(e), p(l), p(i));
    }
  };
}
function tn(n) {
  let e, t;
  return e = new Il({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Zl(e.$$.fragment);
    },
    m(l, i) {
      Hl(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      l[8] === "default"), e.$set(f);
    },
    i(l) {
      t || (x(e.$$.fragment, l), t = !0);
    },
    o(l) {
      $(e.$$.fragment, l), t = !1;
    },
    d(l) {
      jl(e, l);
    }
  };
}
function ln(n) {
  let e, t, l, i, f, s = `${/*last_progress_level*/
  n[15] * 100}%`, o = (
    /*progress*/
    n[7] != null && Oe(n)
  );
  return {
    c() {
      e = T("div"), t = T("div"), o && o.c(), l = P(), i = T("div"), f = T("div"), I(t, "class", "progress-level-inner svelte-14miwb5"), I(f, "class", "progress-bar svelte-14miwb5"), H(f, "width", s), I(i, "class", "progress-bar-wrap svelte-14miwb5"), I(e, "class", "progress-level svelte-14miwb5");
    },
    m(r, a) {
      k(r, e, a), O(e, t), o && o.m(t, null), O(e, l), O(e, i), O(i, f), n[30](f);
    },
    p(r, a) {
      /*progress*/
      r[7] != null ? o ? o.p(r, a) : (o = Oe(r), o.c(), o.m(t, null)) : o && (o.d(1), o = null), a[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      r[15] * 100}%`) && H(f, "width", s);
    },
    i: Ce,
    o: Ce,
    d(r) {
      r && p(e), o && o.d(), n[30](null);
    }
  };
}
function Oe(n) {
  let e, t = me(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = xe(Re(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = ee();
    },
    m(i, f) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, f);
      k(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = me(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const o = Re(i, t, s);
          l[s] ? l[s].p(o, f) : (l[s] = xe(o), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && p(e), mt(l, i);
    }
  };
}
function Je(n) {
  let e, t, l, i, f = (
    /*i*/
    n[40] !== 0 && nn()
  ), s = (
    /*p*/
    n[38].desc != null && Ke(n)
  ), o = (
    /*p*/
    n[38].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null && Qe()
  ), r = (
    /*progress_level*/
    n[14] != null && We(n)
  );
  return {
    c() {
      f && f.c(), e = P(), s && s.c(), t = P(), o && o.c(), l = P(), r && r.c(), i = ee();
    },
    m(a, _) {
      f && f.m(a, _), k(a, e, _), s && s.m(a, _), k(a, t, _), o && o.m(a, _), k(a, l, _), r && r.m(a, _), k(a, i, _);
    },
    p(a, _) {
      /*p*/
      a[38].desc != null ? s ? s.p(a, _) : (s = Ke(a), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      a[38].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[40]
      ] != null ? o || (o = Qe(), o.c(), o.m(l.parentNode, l)) : o && (o.d(1), o = null), /*progress_level*/
      a[14] != null ? r ? r.p(a, _) : (r = We(a), r.c(), r.m(i.parentNode, i)) : r && (r.d(1), r = null);
    },
    d(a) {
      a && (p(e), p(t), p(l), p(i)), f && f.d(a), s && s.d(a), o && o.d(a), r && r.d(a);
    }
  };
}
function nn(n) {
  let e;
  return {
    c() {
      e = F(" /");
    },
    m(t, l) {
      k(t, e, l);
    },
    d(t) {
      t && p(e);
    }
  };
}
function Ke(n) {
  let e = (
    /*p*/
    n[38].desc + ""
  ), t;
  return {
    c() {
      t = F(e);
    },
    m(l, i) {
      k(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[38].desc + "") && V(t, e);
    },
    d(l) {
      l && p(t);
    }
  };
}
function Qe(n) {
  let e;
  return {
    c() {
      e = F("-");
    },
    m(t, l) {
      k(t, e, l);
    },
    d(t) {
      t && p(e);
    }
  };
}
function We(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[40]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = F(e), l = F("%");
    },
    m(i, f) {
      k(i, t, f), k(i, l, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && V(t, e);
    },
    d(i) {
      i && (p(t), p(l));
    }
  };
}
function xe(n) {
  let e, t = (
    /*p*/
    (n[38].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null) && Je(n)
  );
  return {
    c() {
      t && t.c(), e = ee();
    },
    m(l, i) {
      t && t.m(l, i), k(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[38].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[40]
      ] != null ? t ? t.p(l, i) : (t = Je(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && p(e), t && t.d(l);
    }
  };
}
function $e(n) {
  let e, t;
  return {
    c() {
      e = T("p"), t = F(
        /*loading_text*/
        n[9]
      ), I(e, "class", "loading svelte-14miwb5");
    },
    m(l, i) {
      k(l, e, i), O(e, t);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && V(
        t,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && p(e);
    }
  };
}
function fn(n) {
  let e, t, l, i, f;
  const s = [Kl, Jl], o = [];
  function r(a, _) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = r(n)) && (l = o[t] = s[t](n)), {
    c() {
      e = T("div"), l && l.c(), I(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-14miwb5"), z(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), z(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), z(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), z(
        e,
        "border",
        /*border*/
        n[12]
      ), H(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), H(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, _) {
      k(a, e, _), ~t && o[t].m(e, null), n[31](e), f = !0;
    },
    p(a, _) {
      let u = t;
      t = r(a), t === u ? ~t && o[t].p(a, _) : (l && (bt(), $(o[u], 1, 1, () => {
        o[u] = null;
      }), dt()), ~t ? (l = o[t], l ? l.p(a, _) : (l = o[t] = s[t](a), l.c()), x(l, 1), l.m(e, null)) : l = null), (!f || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-14miwb5")) && I(e, "class", i), (!f || _[0] & /*variant, show_progress, status, show_progress*/
      336) && z(e, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!f || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && z(
        e,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!f || _[0] & /*variant, show_progress, status*/
      336) && z(
        e,
        "generating",
        /*status*/
        a[4] === "generating"
      ), (!f || _[0] & /*variant, show_progress, border*/
      4416) && z(
        e,
        "border",
        /*border*/
        a[12]
      ), _[0] & /*absolute*/
      1024 && H(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && H(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      f || (x(l), f = !0);
    },
    o(a) {
      $(l), f = !1;
    },
    d(a) {
      a && p(e), ~t && o[t].d(), n[31](null);
    }
  };
}
let _e = [], ke = !1;
async function sn(n, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (_e.push(n), !ke)
      ke = !0;
    else
      return;
    await Xl(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let l = 0; l < _e.length; l++) {
        const f = _e[l].getBoundingClientRect();
        (l === 0 || f.top + window.scrollY <= t[0]) && (t[0] = f.top + window.scrollY, t[1] = l);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), ke = !1, _e = [];
    });
  }
}
function on(n, e, t) {
  let l, { $$slots: i = {}, $$scope: f } = e, { i18n: s } = e, { eta: o = null } = e, { queue: r = !1 } = e, { queue_position: a } = e, { queue_size: _ } = e, { status: u } = e, { scroll_to_output: c = !1 } = e, { timer: m = !0 } = e, { show_progress: h = "full" } = e, { message: L = null } = e, { progress: q = null } = e, { variant: M = "default" } = e, { loading_text: g = "Loading..." } = e, { absolute: d = !0 } = e, { translucent: C = !1 } = e, { border: w = !1 } = e, { autoscroll: be } = e, te, le = !1, oe = 0, Y = 0, ge = null, qe = 0, U = null, ne, j = null, Fe = !0;
  const ht = () => {
    t(25, oe = performance.now()), t(26, Y = 0), le = !0, Le();
  };
  function Le() {
    requestAnimationFrame(() => {
      t(26, Y = (performance.now() - oe) / 1e3), le && Le();
    });
  }
  function Me() {
    t(26, Y = 0), le && (le = !1);
  }
  Gl(() => {
    le && Me();
  });
  let Se = null;
  function wt(b) {
    Ee[b ? "unshift" : "push"](() => {
      j = b, t(16, j), t(7, q), t(14, U), t(15, ne);
    });
  }
  function pt(b) {
    Ee[b ? "unshift" : "push"](() => {
      te = b, t(13, te);
    });
  }
  return n.$$set = (b) => {
    "i18n" in b && t(1, s = b.i18n), "eta" in b && t(0, o = b.eta), "queue" in b && t(21, r = b.queue), "queue_position" in b && t(2, a = b.queue_position), "queue_size" in b && t(3, _ = b.queue_size), "status" in b && t(4, u = b.status), "scroll_to_output" in b && t(22, c = b.scroll_to_output), "timer" in b && t(5, m = b.timer), "show_progress" in b && t(6, h = b.show_progress), "message" in b && t(23, L = b.message), "progress" in b && t(7, q = b.progress), "variant" in b && t(8, M = b.variant), "loading_text" in b && t(9, g = b.loading_text), "absolute" in b && t(10, d = b.absolute), "translucent" in b && t(11, C = b.translucent), "border" in b && t(12, w = b.border), "autoscroll" in b && t(24, be = b.autoscroll), "$$scope" in b && t(28, f = b.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, queue, timer_start*/
    169869313 && (o === null ? t(0, o = ge) : r && t(0, o = (performance.now() - oe) / 1e3 + o), o != null && (t(19, Se = o.toFixed(1)), t(27, ge = o))), n.$$.dirty[0] & /*eta, timer_diff*/
    67108865 && t(17, qe = o === null || o <= 0 || !Y ? null : Math.min(Y / o, 1)), n.$$.dirty[0] & /*progress*/
    128 && q != null && t(18, Fe = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (q != null ? t(14, U = q.map((b) => {
      if (b.index != null && b.length != null)
        return b.index / b.length;
      if (b.progress != null)
        return b.progress;
    })) : t(14, U = null), U ? (t(15, ne = U[U.length - 1]), j && (ne === 0 ? t(16, j.style.transition = "0", j) : t(16, j.style.transition = "150ms", j))) : t(15, ne = void 0)), n.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? ht() : Me()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && te && c && (u === "pending" || u === "complete") && sn(te, be), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, l = Y.toFixed(1));
  }, [
    o,
    s,
    a,
    _,
    u,
    m,
    h,
    q,
    M,
    g,
    d,
    C,
    w,
    te,
    U,
    ne,
    j,
    qe,
    Fe,
    Se,
    l,
    r,
    c,
    L,
    be,
    oe,
    Y,
    ge,
    f,
    i,
    wt,
    pt
  ];
}
class rn extends Pl {
  constructor(e) {
    super(), Rl(
      this,
      e,
      on,
      fn,
      Yl,
      {
        i18n: 1,
        eta: 0,
        queue: 21,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
new Intl.Collator(0, { numeric: 1 }).compare;
function gt(n, e, t) {
  if (n == null)
    return null;
  if (Array.isArray(n)) {
    const l = [];
    for (const i of n)
      i == null ? l.push(null) : l.push(gt(i, e, t));
    return l;
  }
  return n.is_stream ? t == null ? new ye({
    ...n,
    url: e + "/stream/" + n.path
  }) : new ye({
    ...n,
    url: "/proxy=" + t + "stream/" + n.path
  }) : new ye({
    ...n,
    url: _n(n.path, e, t)
  });
}
function an(n) {
  try {
    const e = new URL(n);
    return e.protocol === "http:" || e.protocol === "https:";
  } catch {
    return !1;
  }
}
function _n(n, e, t) {
  return n == null ? t ? `/proxy=${t}file=` : `${e}/file=` : an(n) ? n : t ? `/proxy=${t}file=${n}` : `${e}/file=${n}`;
}
class ye {
  constructor({
    path: e,
    url: t,
    orig_name: l,
    size: i,
    blob: f,
    is_stream: s,
    mime_type: o,
    alt_text: r
  }) {
    this.path = e, this.url = t, this.orig_name = l, this.size = i, this.blob = t ? void 0 : f, this.is_stream = s, this.mime_type = o, this.alt_text = r;
  }
}
const {
  SvelteComponent: cn,
  assign: un,
  attr: G,
  check_outros: et,
  create_component: ie,
  destroy_component: fe,
  detach: ue,
  element: dn,
  empty: mn,
  get_spread_object: bn,
  get_spread_update: gn,
  group_outros: tt,
  init: hn,
  insert: de,
  mount_component: se,
  noop: lt,
  safe_not_equal: wn,
  space: nt,
  src_url_equal: it,
  transition_in: B,
  transition_out: Z
} = window.__gradio__svelte__internal;
function ft(n) {
  let e, t;
  const l = [
    { autoscroll: (
      /*gradio*/
      n[9].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[9].i18n
    ) },
    /*loading_status*/
    n[8]
  ];
  let i = {};
  for (let f = 0; f < l.length; f += 1)
    i = un(i, l[f]);
  return e = new rn({ props: i }), {
    c() {
      ie(e.$$.fragment);
    },
    m(f, s) {
      se(e, f, s), t = !0;
    },
    p(f, s) {
      const o = s & /*gradio, loading_status*/
      768 ? gn(l, [
        s & /*gradio*/
        512 && { autoscroll: (
          /*gradio*/
          f[9].autoscroll
        ) },
        s & /*gradio*/
        512 && { i18n: (
          /*gradio*/
          f[9].i18n
        ) },
        s & /*loading_status*/
        256 && bn(
          /*loading_status*/
          f[8]
        )
      ]) : {};
      e.$set(o);
    },
    i(f) {
      t || (B(e.$$.fragment, f), t = !0);
    },
    o(f) {
      Z(e.$$.fragment, f), t = !1;
    },
    d(f) {
      fe(e, f);
    }
  };
}
function pn(n) {
  let e, t;
  return e = new ml({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [yn] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      ie(e.$$.fragment);
    },
    m(l, i) {
      se(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i & /*$$scope*/
      32768 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (B(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Z(e.$$.fragment, l), t = !1;
    },
    d(l) {
      fe(e, l);
    }
  };
}
function kn(n) {
  let e, t, l, i;
  return {
    c() {
      e = dn("iframe"), it(e.src, t = /*new_value*/
      n[10].url) || G(e, "src", t), G(e, "title", l = /*label*/
      n[11] ?? "Folium Map"), G(e, "height", i = /*height*/
      n[0] + "px"), G(e, "class", "svelte-1orump4");
    },
    m(f, s) {
      de(f, e, s);
    },
    p(f, s) {
      s & /*new_value*/
      1024 && !it(e.src, t = /*new_value*/
      f[10].url) && G(e, "src", t), s & /*label*/
      2048 && l !== (l = /*label*/
      f[11] ?? "Folium Map") && G(e, "title", l), s & /*height*/
      1 && i !== (i = /*height*/
      f[0] + "px") && G(e, "height", i);
    },
    i: lt,
    o: lt,
    d(f) {
      f && ue(e);
    }
  };
}
function yn(n) {
  let e, t;
  return e = new at({}), {
    c() {
      ie(e.$$.fragment);
    },
    m(l, i) {
      se(e, l, i), t = !0;
    },
    i(l) {
      t || (B(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Z(e.$$.fragment, l), t = !1;
    },
    d(l) {
      fe(e, l);
    }
  };
}
function vn(n) {
  let e, t, l, i, f, s, o, r = (
    /*loading_status*/
    n[8] && ft(n)
  );
  t = new Wt({
    props: {
      show_label: !0,
      Icon: at,
      label: (
        /*label*/
        n[11] || "Folium Map"
      )
    }
  });
  const a = [kn, pn], _ = [];
  function u(c, m) {
    return (
      /*value*/
      c[4] ? 0 : 1
    );
  }
  return i = u(n), f = _[i] = a[i](n), {
    c() {
      r && r.c(), e = nt(), ie(t.$$.fragment), l = nt(), f.c(), s = mn();
    },
    m(c, m) {
      r && r.m(c, m), de(c, e, m), se(t, c, m), de(c, l, m), _[i].m(c, m), de(c, s, m), o = !0;
    },
    p(c, m) {
      /*loading_status*/
      c[8] ? r ? (r.p(c, m), m & /*loading_status*/
      256 && B(r, 1)) : (r = ft(c), r.c(), B(r, 1), r.m(e.parentNode, e)) : r && (tt(), Z(r, 1, 1, () => {
        r = null;
      }), et());
      const h = {};
      m & /*label*/
      2048 && (h.label = /*label*/
      c[11] || "Folium Map"), t.$set(h);
      let L = i;
      i = u(c), i === L ? _[i].p(c, m) : (tt(), Z(_[L], 1, 1, () => {
        _[L] = null;
      }), et(), f = _[i], f ? f.p(c, m) : (f = _[i] = a[i](c), f.c()), B(f, 1), f.m(s.parentNode, s));
    },
    i(c) {
      o || (B(r), B(t.$$.fragment, c), B(f), o = !0);
    },
    o(c) {
      Z(r), Z(t.$$.fragment, c), Z(f), o = !1;
    },
    d(c) {
      c && (ue(e), ue(l), ue(s)), r && r.d(c), fe(t, c), _[i].d(c);
    }
  };
}
function Cn(n) {
  let e, t;
  return e = new Pt({
    props: {
      visible: (
        /*visible*/
        n[3]
      ),
      elem_id: (
        /*elem_id*/
        n[1]
      ),
      elem_classes: (
        /*elem_classes*/
        n[2]
      ),
      container: (
        /*container*/
        n[5]
      ),
      scale: (
        /*scale*/
        n[6]
      ),
      min_width: (
        /*min_width*/
        n[7]
      ),
      $$slots: { default: [vn] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      ie(e.$$.fragment);
    },
    m(l, i) {
      se(e, l, i), t = !0;
    },
    p(l, [i]) {
      const f = {};
      i & /*visible*/
      8 && (f.visible = /*visible*/
      l[3]), i & /*elem_id*/
      2 && (f.elem_id = /*elem_id*/
      l[1]), i & /*elem_classes*/
      4 && (f.elem_classes = /*elem_classes*/
      l[2]), i & /*container*/
      32 && (f.container = /*container*/
      l[5]), i & /*scale*/
      64 && (f.scale = /*scale*/
      l[6]), i & /*min_width*/
      128 && (f.min_width = /*min_width*/
      l[7]), i & /*$$scope, new_value, label, height, value, gradio, loading_status*/
      36625 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (B(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Z(e.$$.fragment, l), t = !1;
    },
    d(l) {
      fe(e, l);
    }
  };
}
function st(n, e) {
  return n ?? e();
}
function qn(n, e, t) {
  let l, { elem_id: i = "" } = e, { elem_classes: f = [] } = e, { visible: s = !0 } = e, { value: o } = e, { container: r = !0 } = e, { scale: a = null } = e, { min_width: _ = void 0 } = e, { loading_status: u } = e, { root: c } = e, { root_url: m } = e, { height: h = 500 } = e, { gradio: L } = e, q;
  async function M() {
    L.dispatch("change");
  }
  return n.$$set = (g) => {
    "elem_id" in g && t(1, i = g.elem_id), "elem_classes" in g && t(2, f = g.elem_classes), "visible" in g && t(3, s = g.visible), "value" in g && t(4, o = g.value), "container" in g && t(5, r = g.container), "scale" in g && t(6, a = g.scale), "min_width" in g && t(7, _ = g.min_width), "loading_status" in g && t(8, u = g.loading_status), "root" in g && t(12, c = g.root), "root_url" in g && t(13, m = g.root_url), "height" in g && t(0, h = g.height), "gradio" in g && t(9, L = g.gradio);
  }, n.$$.update = () => {
    n.$$.dirty & /*label*/
    2048 && t(11, l = st(l, () => "Folium Map")), n.$$.dirty & /*height*/
    1 && t(0, h = st(h, () => 500)), n.$$.dirty & /*value, root, root_url*/
    12304 && t(10, q = { ...gt(o, c, m) }), n.$$.dirty & /*new_value*/
    1024 && M();
  }, [
    h,
    i,
    f,
    s,
    o,
    r,
    a,
    _,
    u,
    L,
    q,
    l,
    c,
    m
  ];
}
class Fn extends cn {
  constructor(e) {
    super(), hn(this, e, qn, Cn, wn, {
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 4,
      container: 5,
      scale: 6,
      min_width: 7,
      loading_status: 8,
      root: 12,
      root_url: 13,
      height: 0,
      gradio: 9
    });
  }
}
export {
  Fn as default
};
