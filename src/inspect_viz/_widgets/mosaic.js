// js/widgets/mosaic.ts
import {
  parseSpec
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm";
import { throttle as throttle3 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";

// js/context/index.ts
import { wasmConnector } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import { InstantiateContext } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm";

// js/inputs/choice.ts
import {
  isParam,
  isSelection,
  clausePoint,
  clausePoints,
  toDataColumns
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import {
  Query
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm";

// js/util/object.ts
var isObject = (v) => {
  return v !== null && typeof v === "object" && !Array.isArray(v);
};

// js/inputs/input.ts
import {
  coordinator,
  MosaicClient
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
function input(InputClass, ...params) {
  const input2 = new InputClass(...params);
  coordinator().connect(input2);
  return input2.element;
}
var Input = class extends MosaicClient {
  element;
  constructor(filterBy) {
    super(filterBy);
    this.element = document.createElement("div");
    Object.defineProperty(this.element, "value", { value: this });
  }
  activate() {
  }
};

// js/util/id.ts
function generateId() {
  return "id-" + Math.random().toString(36).substring(2) + Date.now().toString(36);
}

// js/inputs/util.ts
function createFieldset(legend) {
  const fieldset = window.document.createElement("fieldset");
  if (legend) {
    const legendEl = window.document.createElement("legend");
    legendEl.innerText = legend;
    fieldset.append(legend);
  }
  return fieldset;
}
function setFieldsetOptions(fieldset, options, type) {
  fieldset.querySelectorAll("input, label").forEach((el) => {
    el.remove();
  });
  const name = generateId();
  for (const { value, label } of options || []) {
    const { inputLabel } = createLabeledInput(type, label, name, value);
    fieldset.appendChild(inputLabel);
  }
}
function createLabeledInput(type, label, name, value) {
  const inputLabel = window.document.createElement("label");
  const input2 = window.document.createElement("input");
  input2.type = type;
  if (name) {
    input2.name = name;
  }
  if (value) {
    input2.value = value;
  }
  inputLabel.appendChild(input2);
  inputLabel.appendChild(window.document.createTextNode(` ${label || value}`));
  return { inputLabel, input: input2 };
}
function setupActivationListeners(input2, element) {
  element.addEventListener("pointerenter", (evt) => {
    if (!evt.buttons) input2.activate();
  });
  element.addEventListener("focus", () => input2.activate());
}

// js/inputs/choice.ts
var ChoiceInput = class extends Input {
  constructor(options_) {
    super(options_.filterBy);
    this.options_ = options_;
  }
  data_ = [];
  activate() {
    if (isSelection(this.options_.as) && this.options_.column) {
      const field = this.options_.field || this.options_.column;
      this.options_.as.activate(clausePoint(field, void 0, { source: this }));
    }
  }
  publish(value) {
    const { as, field, column: column2 } = this.options_;
    if (isSelection(as) && column2) {
      let clause = clausePoint(field || column2, void 0, { source: this });
      if (Array.isArray(value) && value.length > 0) {
        clause = clausePoints(
          [field || column2],
          value.map((v) => [v]),
          { source: this }
        );
      } else if (value?.length) {
        clause = clausePoint(field || column2, value, { source: this });
      }
      as.update(clause);
    } else if (isParam(as)) {
      as.update(value);
    }
  }
  query(filter = []) {
    const { from, column: column2 } = this.options_;
    if (!from) {
      return null;
    }
    if (!column2) {
      throw new Error("You must specify a column along with a data source");
    }
    return Query.from(from).select({ value: column2 }).distinct().where(...filter).orderby(column2);
  }
  queryResult(data) {
    if (this.options_.options === void 0) {
      this.setData([{ value: "", label: "All" }, ...this.queryResultOptions(data)]);
    }
    return this;
  }
  queryResultOptions(data) {
    const columns = toDataColumns(data);
    const values = columns.columns.value;
    return values.map((v) => ({ value: v }));
  }
  setOptions(options) {
    this.setData(options.map((opt) => isObject(opt) ? opt : { value: opt }));
    this.update();
  }
  setupParamListener() {
    if (!isSelection(this.options_.as)) {
      this.options_.as.addEventListener("value", (value) => {
        this.selectedValue = value;
      });
    }
  }
  setupActivationListeners(element) {
    if (isSelection(this.options_.as)) {
      setupActivationListeners(this, element);
    }
  }
  updateSelectedValue() {
    const value = isSelection(this.options_.as) ? this.options_.as.valueFor(this) : this.options_.as.value;
    this.selectedValue = value === void 0 ? "" : value;
  }
  setData(options) {
    if (!isSelection(this.options_.as)) {
      const paramValue = this.options_.as.value;
      if (paramValue && !Array.isArray(paramValue) && !options.some((option) => option.value === paramValue)) {
        options = [...options, { value: paramValue }];
      }
    }
    this.data_ = options;
  }
};

// js/inputs/radio_group.ts
var RadioGroup = class extends ChoiceInput {
  fieldset_;
  constructor(options) {
    super(options);
    this.fieldset_ = createFieldset(options.label);
    this.element.append(this.fieldset_);
    if (options.options) {
      this.setOptions(options.options);
    }
    this.selectedValue = "";
    this.fieldset_.addEventListener("change", (e) => {
      if (e.target instanceof HTMLInputElement) {
        if (e.target.type === "radio") {
          this.publish(this.selectedValue ?? null);
        }
      }
    });
    this.setupParamListener();
    this.setupActivationListeners(this.fieldset_);
  }
  get selectedValue() {
    const checked = this.fieldset_.querySelector(
      'input[type="radio"]:checked'
    );
    return checked?.value ? checked.value === "on" ? "" : checked.value : "";
  }
  set selectedValue(value) {
    value = value === "" ? "on" : value;
    const radios = this.fieldset_.querySelectorAll('input[type="radio"]');
    for (const radio of radios) {
      if (radio.value === value) {
        radio.checked = true;
        radio.dispatchEvent(new Event("change", { bubbles: true }));
        break;
      }
    }
  }
  update() {
    setFieldsetOptions(this.fieldset_, this.data_, "radio");
    this.updateSelectedValue();
    return this;
  }
};

// js/inputs/types.ts
var kSidebarFullwidth = "sidebar-fullwidth";
var kInputSearch = "input-search";

// js/inputs/select.ts
import TomSelect from "https://cdn.jsdelivr.net/npm/tom-select@2.4.3/+esm";
import { isSelection as isSelection2 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
var Select = class extends ChoiceInput {
  select_;
  multiple_;
  allowEmpty_;
  initialValue_;
  tomSelect_ = void 0;
  constructor(options) {
    super(options);
    this.multiple_ = options.multiple ?? false;
    this.allowEmpty_ = options.value === "all";
    this.initialValue_ = options.value === "all" || options.value === "auto" ? void 0 : options.value;
    this.element.classList.add(kSidebarFullwidth);
    let labelEl = null;
    if (options.label !== void 0) {
      labelEl = window.document.createElement("label");
      labelEl.innerText = options.label;
      this.element.appendChild(labelEl);
    }
    this.select_ = document.createElement("select");
    if (options.width) {
      this.select_.style.width = `${options.width}px`;
    }
    this.select_.id = generateId();
    if (labelEl) {
      labelEl.appendChild(this.select_);
    } else {
      this.element.appendChild(this.select_);
    }
    if (options.options) {
      this.setOptions(options.options);
    }
    if (this.initialValue_ !== void 0 && isSelection2(this.options_.as)) {
      this.publish(options.value);
    }
    this.select_.addEventListener("input", () => {
      this.publish(this.selectedValue ?? null);
    });
    this.setupParamListener();
    this.setupActivationListeners(this.select_);
  }
  queryResult(data) {
    if (this.options_.options === void 0) {
      if (this.multiple_ || !this.allowEmpty_) {
        this.setData(this.queryResultOptions(data));
        return this;
      } else {
        return super.queryResult(data);
      }
    } else {
      return this;
    }
  }
  get selectedValue() {
    return this.tomSelect_?.getValue() ?? "";
  }
  set selectedValue(value) {
    this.tomSelect_?.setValue(value);
  }
  update() {
    if (!this.tomSelect_) {
      if (this.multiple_) {
        this.select_.multiple = true;
      }
      const config = {
        create: false,
        dropdownParent: "body"
      };
      if (!this.select_.multiple) {
        config.allowEmptyOption = this.allowEmpty_;
        config.controlInput = null;
      } else {
        config.plugins = {
          remove_button: {
            title: "Remove this item"
          }
        };
      }
      this.tomSelect_ = new TomSelect(this.select_, config);
      if (this.multiple_) {
        this.tomSelect_.on("item_add", () => {
          this.tomSelect_.control_input.value = "";
          this.tomSelect_?.refreshOptions(false);
        });
      }
      const defaultValue = this.initialValue_ ?? (this.allowEmpty_ ? "" : this.data_?.[0].value);
      const value = isSelection2(this.options_.as) ? defaultValue : this.options_.as.value || defaultValue;
      this.selectedValue = value;
      this.publish(value);
    }
    this.tomSelect_.clearOptions();
    this.tomSelect_.addOptions(
      this.data_.map((o) => ({ value: o.value, text: o.label || o.value }))
    );
    this.tomSelect_.refreshOptions(false);
    this.updateSelectedValue();
    return this;
  }
};

// js/inputs/checkbox_group.ts
var CheckboxGroup = class extends ChoiceInput {
  fieldset_;
  constructor(options) {
    super(options);
    this.fieldset_ = createFieldset(options.label);
    this.element.append(this.fieldset_);
    if (options.options) {
      this.setOptions(options.options);
    }
    this.fieldset_.addEventListener("change", (e) => {
      if (e.target instanceof HTMLInputElement) {
        if (e.target.type === "checkbox") {
          this.publish(this.selectedValue ?? []);
        }
      }
    });
    this.setupParamListener();
    this.setupActivationListeners(this.fieldset_);
  }
  get selectedValue() {
    const checked = this.fieldset_.querySelectorAll(
      'input[type="checkbox"]:checked'
    );
    return Array.from(checked).map((checkbox) => checkbox.value);
  }
  set selectedValue(values) {
    const checkboxes = this.fieldset_.querySelectorAll('input[type="checkbox"]');
    for (const checkbox of checkboxes) {
      const input2 = checkbox;
      const shouldBeChecked = values.includes(input2.value);
      if (input2.checked !== shouldBeChecked) {
        input2.checked = shouldBeChecked;
        input2.dispatchEvent(new Event("change", { bubbles: true }));
      }
    }
  }
  queryResult(data) {
    if (this.options_.options === void 0) {
      this.setData(this.queryResultOptions(data));
    }
    return this;
  }
  update() {
    setFieldsetOptions(this.fieldset_, this.data_, "checkbox");
    this.updateSelectedValue();
    return this;
  }
};

// js/inputs/checkbox.ts
import {
  clausePoint as clausePoint2,
  isParam as isParam2,
  isSelection as isSelection3
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
var Checkbox = class extends Input {
  constructor(options_) {
    super(options_.filterBy);
    this.options_ = options_;
    const { inputLabel, input: input2 } = createLabeledInput("checkbox", options_.label);
    input2.id = generateId();
    this.element.appendChild(inputLabel);
    input2.checked = !isSelection3(this.options_.as) ? this.options_.as?.value ?? options_.checked : options_.checked;
    const publish = () => this.publish(
      input2.checked ? options_.values[0] || void 0 : options_.values[1] || void 0
    );
    input2.addEventListener("change", publish);
    publish();
    if (!isSelection3(this.options_.as)) {
      this.options_.as.addEventListener("value", (value) => {
        input2.checked = value === this.options_.values[0];
      });
    } else {
      setupActivationListeners(this, input2);
    }
  }
  activate() {
    if (isSelection3(this.options_.as)) {
      this.options_.as.activate(this.clause());
    }
  }
  clause(value) {
    if (!this.options_.field) {
      throw new Error("checkbox 'field' option must be specified with selection");
    }
    return clausePoint2(this.options_.field, value, { source: this });
  }
  publish(value) {
    if (isSelection3(this.options_.as)) {
      this.options_.as.update(this.clause(value));
    } else if (isParam2(this.options_.as)) {
      this.options_.as.update(value);
    }
  }
};

// js/inputs/slider.ts
import {
  clauseInterval,
  clausePoint as clausePoint3,
  isParam as isParam3,
  isSelection as isSelection4
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import {
  max,
  min,
  Query as Query2
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm";
import {
  create as createSlider
} from "https://cdn.jsdelivr.net/npm/nouislider@15.8.1/+esm";
var kSliderInput = "slider-input";
var Slider = class extends Input {
  constructor(options_) {
    super(options_.filterBy);
    this.options_ = options_;
    this.element.classList.add(kSliderInput, kSidebarFullwidth);
    const id = generateId();
    const label = options_.label;
    let container = this.element;
    if (label) {
      container = window.document.createElement("label");
      container.innerText = label;
      this.element.appendChild(container);
    }
    let { value, width, min: min3, max: max3 } = options_;
    this.slider_ = document.createElement("div");
    this.slider_.classList.add("noUi-round");
    this.slider_.setAttribute("id", id);
    if (width != void 0) {
      this.slider_.style.width = `${+width}px`;
    }
    if (container) {
      container.appendChild(this.slider_);
    } else {
      this.element.appendChild(this.slider_);
    }
    this.sliderApi_ = createSlider(this.slider_, {
      range: { min: 0, max: 0 },
      connect: options_.select === "interval",
      start: options_.select === "interval" ? [0, 0] : 0
    });
    this.curval_ = document.createElement("label");
    this.curval_.setAttribute("class", "slider-value");
    this.element.appendChild(this.curval_);
    if (this.options_.as?.value === void 0) {
      this.publish(value);
    } else if (value === void 0) {
      value = this.options_.as?.value;
    }
    this.updateCurrentValue();
    if (!isSelection4(this.options_.as)) {
      this.options_.as.addEventListener("value", (value2) => {
        if (!areEqual(value2, this.sliderValue)) {
          this.sliderApi_.set(value2);
          this.updateCurrentValue();
        }
      });
    } else {
      setupActivationListeners(this, this.slider_);
    }
    if (!options_.from) {
      min3 = min3 ?? (Array.isArray(value) ? value[0] : value ?? 0);
      max3 = max3 ?? (Array.isArray(value) ? value[1] : value ?? 0);
      const start = value ?? (options_.select === "interval" ? [0, 0] : 0);
      this.updateSlider(min3, max3, start);
      this.sliderApi_.on("update", () => {
        this.updateCurrentValue();
        this.publish(this.sliderValue);
      });
    }
  }
  slider_;
  sliderApi_;
  curval_;
  firstQuery_ = false;
  updateCurrentValue() {
    const value = this.sliderValue;
    if (Array.isArray(value)) {
      this.curval_.innerText = `${value[0].toLocaleString()}-${value[1].toLocaleString()}`;
    } else {
      this.curval_.innerHTML = value.toLocaleString();
    }
  }
  get sliderValue() {
    const value = this.sliderApi_.get();
    if (Array.isArray(value)) {
      return value.map(cleanNumber).slice(0, 2);
    } else {
      return cleanNumber(value);
    }
  }
  set sliderValue(value) {
    this.sliderApi_.set(value, true);
  }
  activate() {
    const target = this.options_.as;
    if (isSelection4(target)) {
      target.activate(this.clause());
    }
  }
  query(filter = []) {
    const { from, column: column2 } = this.options_;
    if (!from || !column2) {
      return null;
    }
    return Query2.select({ min: min(column2), max: max(column2) }).from(from).where(...filter);
  }
  queryResult(data) {
    const { min: dataMin, max: dataMax } = Array.from(data)[0];
    const min3 = this.options_.min ?? dataMin;
    const max3 = this.options_.max ?? dataMax;
    let start = this.sliderValue;
    if (!this.firstQuery_) {
      this.firstQuery_ = true;
      if (this.options_.value === void 0) {
        start = this.options_.select === "interval" ? [min3, max3] : max3;
      } else {
        start = this.options_.value;
      }
      this.updateSlider(min3, max3, start);
      this.sliderApi_.on("update", () => {
        this.updateCurrentValue();
        this.publish(this.sliderValue);
      });
    } else {
      this.updateSlider(min3, max3, start);
    }
    return this;
  }
  updateSlider(min3, max3, start) {
    const step = this.options_.step ?? (min3 >= 5 || max3 >= 5 ? 1 : void 0);
    this.sliderApi_.updateOptions(
      {
        range: {
          min: min3,
          max: max3
        },
        step,
        start
      },
      true
    );
    return this;
  }
  clause(value) {
    let { field, column: column2, min: min3, select = "point" } = this.options_;
    field = field || column2;
    if (!field) {
      throw new Error(
        "You must specify a 'column' or 'field' for a slider targeting a selection."
      );
    }
    if (select === "interval" && value !== void 0) {
      const domain = Array.isArray(value) ? value : [min3 ?? 0, value];
      return clauseInterval(field, domain, {
        source: this,
        bin: "ceil",
        scale: { type: "identity", domain },
        pixelSize: this.options_.step || void 0
      });
    } else {
      return clausePoint3(field, Array.isArray(value) ? value[0] : value, {
        source: this
      });
    }
  }
  publish(value) {
    const target = this.options_.as;
    if (isSelection4(target)) {
      target.update(this.clause(value));
    } else if (isParam3(target)) {
      target.update(value);
    }
  }
};
function areEqual(a, b) {
  if (Array.isArray(a) && Array.isArray(b)) {
    return a.map(cleanNumber) === b.map(cleanNumber);
  } else if (!Array.isArray(a) && !Array.isArray(b)) {
    return cleanNumber(a) === cleanNumber(b);
  } else {
    return false;
  }
}
function cleanNumber(num) {
  if (typeof num === "string") {
    num = parseFloat(num);
  }
  if (!isFinite(num)) return num;
  if (num === 0) return 0;
  const magnitude = Math.abs(num);
  const epsilon = magnitude * Number.EPSILON * 100;
  const rounded = Math.round(num);
  if (Math.abs(num - rounded) < epsilon) {
    return rounded;
  }
  return parseFloat(num.toPrecision(15));
}

// js/inputs/table.ts
import {
  clausePoints as clausePoints2,
  isSelection as isSelection5,
  queryFieldInfo,
  throttle,
  toDataColumns as toDataColumns2
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import {
  and,
  asc,
  contains,
  desc,
  eq,
  gt,
  gte,
  isNull,
  literal,
  lt,
  lte,
  neq,
  not,
  or,
  prefix,
  suffix,
  Query as Query3,
  sql,
  column,
  avg,
  count,
  sum,
  argmax,
  mad,
  max as max2,
  min as min2,
  product,
  geomean,
  median,
  mode,
  variance,
  stddev,
  skewness,
  kurtosis,
  entropy,
  varPop,
  stddevPop,
  first,
  last,
  stringAgg,
  arrayAgg,
  argmin,
  quantile,
  corr,
  covarPop,
  regrIntercept,
  regrSlope,
  regrCount,
  regrR2,
  regrSXX,
  regrSYY,
  regrSXY,
  regrAvgX,
  regrAvgY
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm";
import {
  createGrid,
  ModuleRegistry,
  AllCommunityModule,
  themeBalham
} from "https://cdn.jsdelivr.net/npm/ag-grid-community@33.3.2/+esm";
import * as d3Format from "https://cdn.jsdelivr.net/npm/d3-format@3.1.0/+esm";
import * as d3TimeFormat from "https://cdn.jsdelivr.net/npm/d3-time-format@4.1.0/+esm";
var kAutoRowCount = 12;
var kAutoRowMaxHeight = 380;
var Table = class extends Input {
  constructor(options_) {
    super(options_.filter_by);
    this.options_ = options_;
    ModuleRegistry.registerModules([AllCommunityModule]);
    this.id_ = generateId();
    this.currentRow_ = -1;
    this.element.classList.add("inspect-viz-table");
    if (typeof this.options_.width === "number") {
      this.element.style.width = `${this.options_.width}px`;
    }
    if (this.options_.max_width) {
      this.element.style.maxWidth = `${this.options_.max_width}px`;
    }
    if (this.options_.auto_filling) {
      this.element.style.height = `100%`;
    } else if (this.options_.height && this.options_.height !== "auto") {
      this.element.style.height = `${this.options_.height}px`;
    }
    if (this.options_.style) {
      if (this.options_.style?.background_color) {
        this.element.style.setProperty(
          "--ag-background-color",
          this.options_.style.background_color
        );
      }
      if (this.options_.style?.foreground_color) {
        this.element.style.setProperty(
          "--ag-foreground-color",
          this.options_.style.foreground_color
        );
      }
      if (this.options_.style?.accent_color) {
        this.element.style.setProperty(
          "--ag-accent-color",
          this.options_.style.accent_color
        );
      }
    }
    this.gridContainer_ = document.createElement("div");
    this.gridContainer_.id = this.id_;
    this.gridContainer_.style.width = "100%";
    this.gridContainer_.style.height = "100%";
    this.element.appendChild(this.gridContainer_);
    this.gridOptions_ = this.createGridOptions(this.options_);
  }
  id_;
  columns_ = [];
  columnsByName_ = {};
  columnTypes_ = {};
  gridContainer_;
  grid_ = null;
  gridOptions_;
  currentRow_;
  sortModel_ = [];
  filterModel_ = {};
  data_ = {
    numRows: 0,
    columns: {}
  };
  // contribute a selection clause back to the target selection
  clause(rows = []) {
    const fields = this.getDatabaseColumns().map((column2) => column2.column_id);
    const values = rows.map((row) => {
      return fields.map((f) => this.data_.columns[f][row]);
    });
    return clausePoints2(fields, values, { source: this });
  }
  // mosaic calls this and initialization to let us fetch the schema
  // and do related setup
  async prepare() {
    const table = this.options_.from;
    const schema = await queryFieldInfo(this.coordinator, [{ column: "*", table }]);
    const userColumns = this.options_.columns ? this.options_.columns : schema.map((f) => f.column);
    this.columns_ = resolveColumns(userColumns);
    this.columnsByName_ = this.columns_.reduce(
      (acc, col) => {
        acc[col.column_name] = col;
        return acc;
      },
      {}
    );
    this.columns_.filter((c) => c.type !== "literal").forEach((column2) => {
      const item = schema.find((s) => s.column === column2.column_id);
      if (item) {
        this.columnTypes_[column2.column_name] = item.type;
      }
    });
    this.getLiteralColumns().forEach((c) => {
      const colVal = c.column;
      if (Array.isArray(colVal)) {
        const firstVal = colVal[0];
        const typeStr = typeof firstVal === "boolean" ? "boolean" : typeof firstVal === "number" ? "number" : void 0;
        if (typeStr) {
          this.columnTypes_[c.column_name] = typeStr;
        }
      } else if (typeof colVal === "boolean") {
        this.columnTypes_[c.column_name] = "boolean";
      } else if (typeof colVal === "number") {
        this.columnTypes_[c.column_name] = "number";
      }
    });
    const columnDefs = this.columns_.map((column2) => {
      const t = this.columnTypes_[column2.column_name];
      return this.createColumnDef(column2.column_name, t);
    });
    this.gridOptions_.columnDefs = columnDefs;
    this.grid_ = createGrid(this.gridContainer_, this.gridOptions_);
  }
  // mosaic calls this every time it needs to show data to find
  // out what query we want to run
  query(filter = []) {
    const selectItems = {};
    const groupBy = [];
    let has_aggregate = false;
    for (const column2 of this.getDatabaseColumns()) {
      if (column2.type === "aggregate") {
        const item = aggregateExpression(column2);
        selectItems[item[0]] = item[1];
        has_aggregate = true;
      } else if (column2.type === "column") {
        selectItems[column2.column_id] = column2.column_id;
        groupBy.push(column2.column_id);
      }
    }
    let query = Query3.from(this.options_.from).select(
      Object.keys(selectItems).length ? selectItems : "*"
    );
    if (has_aggregate && groupBy.length > 0) {
      query.groupby(groupBy);
    }
    query = query.where(...filter);
    Object.keys(this.filterModel_).forEach((columnName) => {
      const col = this.columnsByName_[columnName] || {};
      if (col.type !== "literal") {
        const useHaving = col.type === "aggregate";
        const filter2 = this.filterModel_[columnName];
        const expression = filterExpression(columnName, filter2, query);
        if (expression) {
          if (useHaving) {
            query.having(expression);
          } else {
            query = query.where(expression);
          }
        }
      }
    });
    if (this.sortModel_.length > 0) {
      this.sortModel_.forEach((sort) => {
        const col = this.columnsByName_[sort.colId] || {};
        if (col.type !== "literal") {
          query = query.orderby(sort.sort === "asc" ? asc(sort.colId) : desc(sort.colId));
        }
      });
    }
    return query;
  }
  // mosaic returns the results of the query() in this function.
  queryResult(data) {
    this.data_ = toDataColumns2(data);
    return this;
  }
  // requests a client UI update (e.g. to reflect results from a query)
  update() {
    this.updateGrid(null);
    return this;
  }
  updateGrid = throttle(async () => {
    if (!this.grid_) {
      return;
    }
    const rowData = [];
    for (let i = 0; i < this.data_.numRows; i++) {
      const row = {};
      this.columns_.forEach(({ column_name, column: column2 }) => {
        if (Array.isArray(column2)) {
          const index = i % column2.length;
          row[column_name] = column2[index];
        } else if (typeof column2 === "boolean" || typeof column2 === "number") {
          row[column_name] = column2;
        } else {
          row[column_name] = this.data_.columns[column_name][i];
        }
      });
      rowData.push(row);
    }
    this.grid_.setGridOption("rowData", rowData);
    if (this.data_.numRows < kAutoRowCount && this.options_.height === void 0) {
      this.grid_.setGridOption("domLayout", "autoHeight");
    } else if (!this.options_.auto_filling && (this.options_.height === "auto" || this.options_.height === void 0)) {
      this.element.style.height = `${kAutoRowMaxHeight}px`;
    }
  });
  createGridOptions(options) {
    const headerHeightPixels = typeof options.header_height === "string" ? void 0 : options.header_height;
    const hoverSelect = options.select === "hover";
    const explicitSelection = resolveRowSelection(options);
    const gridTheme = themeBalham.withParams({
      textColor: this.options_.style?.text_color,
      headerTextColor: this.options_.style?.header_text_color || this.options_.style?.text_color,
      cellTextColor: this.options_.style?.cell_text_color,
      fontFamily: this.options_.style?.font_family,
      headerFontFamily: this.options_.style?.header_font_family || this.options_.style?.font_family,
      cellFontFamily: this.options_.style?.cell_font_family || this.options_.style?.font_family,
      spacing: this.options_.style?.spacing || 4,
      borderColor: this.options_.style?.border_color,
      borderRadius: this.options_.style?.border_radius,
      selectedRowBackgroundColor: this.options_.style?.selected_row_background_color
    });
    const domLayout = this.options_.height === "auto" ? "autoHeight" : void 0;
    return {
      // always pass filter to allow server-side filtering
      pagination: !!options.pagination,
      paginationAutoPageSize: options.pagination?.page_size === "auto" || options.pagination?.page_size === void 0,
      paginationPageSizeSelector: options.pagination?.page_size_selector,
      paginationPageSize: typeof options.pagination?.page_size === "number" ? options.pagination.page_size : void 0,
      animateRows: false,
      headerHeight: headerHeightPixels,
      rowHeight: options.row_height,
      domLayout,
      columnDefs: [],
      rowData: [],
      rowSelection: explicitSelection,
      suppressCellFocus: true,
      enableCellTextSelection: true,
      theme: gridTheme,
      onFilterChanged: () => {
        this.filterModel_ = this.grid_?.getFilterModel() || {};
        this.requestQuery();
      },
      onSortChanged: () => {
        if (this.grid_) {
          const sortModel = this.grid_.getColumnState().filter((col) => col.sort).map((col) => ({ colId: col.colId, sort: col.sort }));
          this.sortModel_ = sortModel;
          this.requestQuery();
        }
      },
      onSelectionChanged: (event) => {
        if (explicitSelection !== void 0 && isSelection5(this.options_.as)) {
          if (event.selectedNodes) {
            const rowIndices = event.selectedNodes.map((n) => n.rowIndex).filter((n) => n !== null);
            this.options_.as.update(this.clause(rowIndices));
          }
        }
      },
      onCellMouseOver: (event) => {
        if (hoverSelect && isSelection5(this.options_.as)) {
          const rowIndex = event.rowIndex;
          if (rowIndex !== void 0 && rowIndex !== null && rowIndex !== this.currentRow_) {
            this.currentRow_ = rowIndex;
            this.options_.as.update(this.clause([rowIndex]));
          }
        }
      },
      onCellMouseOut: () => {
        if (hoverSelect && isSelection5(this.options_.as)) {
          this.currentRow_ = -1;
          this.options_.as.update(this.clause());
        }
      },
      onGridReady: () => {
        this.patchGrid();
      }
    };
  }
  getLiteralColumns() {
    return this.columns_.filter((c) => c.type === "literal");
  }
  getDatabaseColumns() {
    return this.columns_.filter((c) => c.type === "column" || c.type === "aggregate");
  }
  createColumnDef(column_name, type) {
    const column2 = this.columnsByName_[column_name] || {};
    const align = column2.align || (type === "number" ? "right" : "left");
    const headerAlignment = column2.header_align;
    const formatter = formatterForType(type, column2.format);
    const sortable = this.options_.sorting !== false && column2.sortable !== false;
    const filterable = this.options_.filtering !== false && column2.filterable !== false;
    const resizable = column2.resizable !== false;
    const minWidth = column2.min_width;
    const maxWidth = column2.max_width;
    const autoHeight = column2.auto_height;
    const autoHeaderHeight = this.options_.header_height === "auto" && column2.header_auto_height !== false;
    const wrapText = column2.wrap_text;
    const wrapHeaderText = column2.header_wrap_text;
    const flex = column2.flex;
    const disableClientSort = (_valueA, _valueB) => {
      return 0;
    };
    const filter = filterable ? filterForColumnType(type) : void 0;
    const colDef = {
      field: column_name,
      headerName: column2.label || column_name,
      headerClass: headerClasses(headerAlignment),
      cellStyle: { textAlign: align },
      comparator: column2.type !== "literal" ? disableClientSort : void 0,
      filter: filter?.filter,
      filterParams: filter?.filterParams,
      flex,
      sortable,
      resizable,
      minWidth,
      maxWidth,
      autoHeight,
      autoHeaderHeight,
      wrapText,
      wrapHeaderText,
      floatingFilter: this.options_.filtering === "row",
      // Disable column moving
      suppressMovable: true,
      valueFormatter: (params) => {
        const value = params.value;
        if (formatter && value !== null && value !== void 0) {
          return formatter(value);
        }
        return value;
      }
    };
    const width = column2.width;
    if (width) {
      colDef.width = width;
    } else if (flex === void 0 || flex === null) {
      colDef.flex = 1;
    }
    return colDef;
  }
  patchGrid() {
    if (!this.grid_) {
      return;
    }
    const columns = this.grid_.getColumns();
    if (columns) {
      columns.forEach(async (column2) => {
        const colId = column2.getColId();
        const filterInstance = await this.grid_.getColumnFilterInstance(colId);
        const col = this.columnsByName_[colId] || {};
        if (filterInstance && typeof filterInstance.doesFilterPass === "function" && col.type !== "literal") {
          filterInstance.doesFilterPass = () => true;
        }
      });
    }
  }
  // all mosaic inputs implement this, not exactly sure what it does
  activate() {
    if (isSelection5(this.options_.as)) {
      this.options_.as.activate(this.clause([]));
    }
  }
};
var resolveColumns = (columns) => {
  let columnCount = 1;
  const incrementedColumnName = () => {
    return `col_${columnCount++}`;
  };
  return columns.map((col) => {
    if (typeof col === "string") {
      return {
        column_name: col,
        column_id: col,
        column: col,
        type: "column"
      };
    } else if (typeof col === "object" && col !== null) {
      if (typeof col.column === "string") {
        return {
          ...col,
          column_name: col.column,
          column_id: col.column,
          type: "column"
        };
      } else if (typeof col.column === "number") {
        return {
          ...col,
          column_name: incrementedColumnName(),
          column: col.column,
          type: "literal"
        };
      } else if (typeof col.column === "boolean") {
        return {
          ...col,
          column_name: incrementedColumnName(),
          column: col.column,
          type: "literal"
        };
      } else if (Array.isArray(col.column)) {
        if (col.column.length === 0) {
          throw new Error("Empty array column is not supported");
        }
        return {
          ...col,
          column_name: incrementedColumnName(),
          column: col.column,
          type: "literal"
        };
      } else if (typeof col.column === "object") {
        const agg = Object.keys(col.column)[0];
        const targetColumn = col.column[agg];
        return {
          ...col,
          column_name: `${agg}_${targetColumn}`,
          column_id: targetColumn,
          agg_expr: agg,
          agg_expr_args: [targetColumn],
          type: "aggregate"
        };
      } else {
        throw new Error("Unsupported column type: " + typeof col.column);
      }
    } else {
      throw new Error(`Invalid column definition: ${col}`);
    }
  });
};
var headerClasses = (align) => {
  if (!align) {
    return void 0;
  }
  return [`header-${align}`];
};
var resolveRowSelection = (options) => {
  if (options.select === "hover") {
    return void 0;
  }
  const selectType = options.select || "single_row";
  if (selectType.startsWith("single_")) {
    return {
      mode: "singleRow",
      checkboxes: options.select === "single_checkbox",
      enableClickSelection: options.select === "single_row"
    };
  } else if (selectType.startsWith("multiple_")) {
    return {
      mode: "multiRow",
      selectAll: "filtered",
      checkboxes: options.select === "multiple_checkbox"
    };
  } else {
    throw new Error("Invalid select option: " + options.select);
  }
};
var filterForColumnType = (type) => {
  switch (type) {
    case "number":
    case "integer":
    case "float":
    case "decimal":
      return { filter: "agNumberColumnFilter" };
    case "date":
    case "datetime":
    case "timestamp":
      return { filter: "agDateColumnFilter" };
    case "boolean":
      return {
        filter: "agTextColumnFilter",
        filterParams: {
          filterOptions: ["equals"],
          textMatcher: ({ filterText, value }) => {
            const stringValue = String(value);
            return stringValue === filterText;
          }
        }
      };
    default:
      return { filter: "agTextColumnFilter" };
  }
};
var formatterForType = (type, formatStr) => {
  switch (type) {
    case "integer":
      return d3Format.format(formatStr || ",");
    case "number":
    case "float":
      return d3Format.format(formatStr || ",.2~f");
    case "decimal":
      return d3Format.format(formatStr || ",.4~f");
    case "date":
      return d3TimeFormat.timeFormat(formatStr || "%Y-%m-%d");
    case "datetime":
    case "timestamp":
      return d3TimeFormat.timeFormat(formatStr || "%Y-%m-%d %H:%M:%S");
    case "boolean":
    case "string":
    default:
      return void 0;
  }
};
var filterExpression = (colId, filter, query) => {
  if (isCombinedSimpleModel(filter)) {
    const operator = filter.operator === "AND" ? and : or;
    const expressions = filter.conditions?.map((f) => {
      return filterExpression(colId, f, query);
    }).filter((e) => e !== void 0);
    if (expressions && expressions.length > 0) {
      return operator(...expressions);
    }
  } else if (isTextFilter(filter)) {
    return simpleExpression(colId, filter.type, filter.filter, void 0, true);
  } else if (isNumberFilter(filter)) {
    return simpleExpression(colId, filter.type, filter.filter);
  } else if (isMultiFilter(filter)) {
    const expr = filter.filterModels?.map((f) => {
      return filterExpression(colId, f, query);
    }).filter((e) => e !== void 0);
    if (expr && expr.length > 0) {
      return and(...expr);
    }
  } else if (isDateFilter(filter)) {
    return simpleExpression(colId, filter.type, filter.dateFrom, filter.dateTo || void 0);
  } else if (isSetFilter(filter)) {
    console.warn("Set filter not implemented");
  }
};
var simpleExpression = (colId, type, filter, filterTo = void 0, textColumn = false) => {
  switch (type) {
    case "equals":
      return eq(colId, literal(filter));
    case "notEqual":
      return neq(colId, literal(filter));
    case "contains":
      if (textColumn) {
        return sql`${column(colId)} ILIKE ${literal("%" + filter + "%")}`;
      } else {
        return contains(colId, String(filter));
      }
    case "notContains":
      return not(contains(colId, String(filter)));
    case "blank":
      return isNull(colId);
    case "notBlank":
      return not(isNull(colId));
    case "startsWith":
      return prefix(colId, String(filter));
    case "endsWith":
      return suffix(colId, String(filter));
    case "greaterThan":
      return gt(colId, literal(filter));
    case "lessThan":
      return lt(colId, literal(filter));
    case "greaterThanOrEqual":
      return gte(colId, literal(filter));
    case "lessThanOrEqual":
      return lte(colId, literal(filter));
    case "inRange":
      if (filterTo !== void 0 && filterTo !== null) {
        return gte(colId, literal(filter)), lte(colId, literal(filterTo));
      }
      break;
    default:
      console.warn(`Unsupported filter type: ${type}`);
  }
  return void 0;
};
var aggregateExpression = (c) => {
  const aggExpr = c.agg_expr;
  const firstArg = () => {
    if (c.agg_expr_args.length > 0) {
      return c.agg_expr_args[0];
    }
    throw new Error(`Aggregate expression ${aggExpr} requires at least one argument`);
  };
  const secondArg = () => {
    if (c.agg_expr_args.length > 1) {
      return c.agg_expr_args[1];
    }
    throw new Error(`Aggregate expression ${aggExpr} requires at least two arguments`);
  };
  const r = (val) => {
    return [c.column_name, val];
  };
  switch (aggExpr) {
    case "count":
      return r(count(firstArg()));
    case "sum":
      return r(sum(firstArg()));
    case "avg":
      return r(avg(firstArg()));
    case "argmax":
      return r(argmax(firstArg(), secondArg()));
    case "mad":
      return r(mad(firstArg()));
    case "max":
      return r(max2(firstArg()));
    case "min":
      return r(min2(firstArg()));
    case "product":
      return r(product(firstArg()));
    case "geomean":
      return r(geomean(firstArg()));
    case "median":
      return r(median(firstArg()));
    case "mode":
      return r(mode(firstArg()));
    case "variance":
      return r(variance(firstArg()));
    case "stddev":
      return r(stddev(firstArg()));
    case "skewness":
      return r(skewness(firstArg()));
    case "kurtosis":
      return r(kurtosis(firstArg()));
    case "entropy":
      return r(entropy(firstArg()));
    case "varPop":
      return r(varPop(firstArg()));
    case "stddevPop":
      return r(stddevPop(firstArg()));
    case "first":
      return r(first(firstArg()));
    case "last":
      return r(last(firstArg()));
    case "stringAgg":
      return r(stringAgg(firstArg()));
    case "arrayAgg":
      return r(arrayAgg(firstArg()));
    case "argmin":
      return r(argmin(firstArg(), secondArg()));
    case "quantile":
      return r(quantile(firstArg(), secondArg()));
    case "corr":
      return r(corr(firstArg(), secondArg()));
    case "covarPop":
      return r(covarPop(firstArg(), secondArg()));
    case "regrIntercept":
      return r(regrIntercept(firstArg(), secondArg()));
    case "regrSlope":
      return r(regrSlope(firstArg(), secondArg()));
    case "regrCount":
      return r(regrCount(firstArg(), secondArg()));
    case "regrR2":
      return r(regrR2(firstArg(), secondArg()));
    case "regrSXX":
      return r(regrSXX(firstArg(), secondArg()));
    case "regrSYY":
      return r(regrSYY(firstArg(), secondArg()));
    case "regrSXY":
      return r(regrSXY(firstArg(), secondArg()));
    case "regrAvgX":
      return r(regrAvgX(firstArg(), secondArg()));
    case "regrAvgY":
      return r(regrAvgY(firstArg(), secondArg()));
    default:
      throw new Error(`Unsupported aggregate expression: ${aggExpr}.`);
  }
};
var isCombinedSimpleModel = (filter) => {
  return typeof filter === "object" && filter !== null && "operator" in filter && "conditions" in filter && (filter.operator === "AND" || filter.operator === "OR") && typeof filter.conditions === "object";
};
var isTextFilter = (filter) => {
  return filter?.filterType === "text";
};
var isNumberFilter = (filter) => {
  return filter?.filterType === "number";
};
var isDateFilter = (filter) => {
  return filter?.filterType === "date" || filter?.filterType === "dateString";
};
var isMultiFilter = (filter) => {
  return filter?.filterType === "multi" && "filterModels" in filter;
};
var isSetFilter = (filter) => {
  return filter?.filterType === "set";
};

// js/inputs/search.ts
import {
  clauseMatch,
  isParam as isParam4,
  isSelection as isSelection6
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm";
import { Query as Query4 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm";
var Search = class extends Input {
  constructor(options_) {
    super(options_.filterBy);
    this.options_ = options_;
    this.element.classList.add(kSidebarFullwidth);
    if (options_.label) {
      const inputLabel = window.document.createElement("label");
      inputLabel.setAttribute("for", this.id_);
      inputLabel.innerText = options_.label;
      this.element.appendChild(inputLabel);
    }
    this.input_ = window.document.createElement("input");
    this.input_.autocomplete = "off";
    this.input_.classList.add(kInputSearch);
    this.input_.id = this.id_;
    this.input_.type = "text";
    if (this.options_.placeholder) {
      this.input_.setAttribute("placeholder", this.options_.placeholder);
    }
    if (this.options_.width) {
      this.input_.style.width = `${options_.width}px`;
    }
    this.element.appendChild(this.input_);
    this.input_.addEventListener("input", () => {
      this.publish(this.input_.value);
    });
    if (!isSelection6(this.options_.as)) {
      this.options_.as.addEventListener("value", (value) => {
        if (value !== this.input_.value) {
          this.input_.value = value;
        }
      });
    } else {
      setupActivationListeners(this, this.input_);
    }
  }
  input_;
  id_ = generateId();
  data_ = [];
  datalist_;
  reset() {
    this.input_.value = "";
  }
  clause(value) {
    const field = this.options_.field || this.options_.column;
    return clauseMatch(field, value, { source: this, method: this.options_.type });
  }
  activate() {
    if (isSelection6(this.options_.as)) {
      this.options_.as.activate(this.clause(""));
    }
  }
  publish(value) {
    if (isSelection6(this.options_.as)) {
      this.options_.as.update(this.clause(value));
    } else if (isParam4(this.options_.as)) {
      this.options_.as.update(value);
    }
  }
  query(filter = []) {
    return Query4.from(this.options_.from).select({ list: this.options_.column }).distinct().where(...filter);
  }
  queryResult(data) {
    this.data_ = data;
    return this;
  }
  update() {
    const list = document.createElement("datalist");
    const id = `${this.id_}_list`;
    list.setAttribute("id", id);
    for (const d of this.data_) {
      const opt = document.createElement("option");
      opt.setAttribute("value", d.list);
      list.append(opt);
    }
    if (this.datalist_) {
      this.datalist_.remove();
    }
    this.element.appendChild(this.datalist_ = list);
    this.input_.setAttribute("list", id);
    return this;
  }
};

// js/inputs/index.ts
var INPUTS = {
  select: (options) => input(Select, options),
  slider: (options) => input(Slider, options),
  search: (options) => input(Search, options),
  checkbox: (options) => input(Checkbox, options),
  radio_group: (options) => input(RadioGroup, options),
  checkbox_group: (options) => input(CheckboxGroup, options),
  table: (options) => input(Table, options)
};

// js/context/duckdb.ts
import {
  getJsDelivrBundles,
  selectBundle,
  AsyncDuckDB,
  ConsoleLogger,
  LogLevel
} from "https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm";

// js/util/async.ts
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
function throttle2(func, wait, options = {}) {
  let context;
  let args;
  let result;
  let timeout = null;
  let previous = 0;
  const later = function() {
    previous = options.leading === false ? 0 : Date.now();
    timeout = null;
    result = func.apply(context, args === null ? [] : args);
    if (!timeout) {
      context = null;
      args = null;
    }
  };
  return function(...callArgs) {
    const now = Date.now();
    if (!previous && options.leading === false) {
      previous = now;
    }
    const remaining = wait - (now - previous);
    context = this;
    args = callArgs;
    if (remaining <= 0 || remaining > wait) {
      if (timeout) {
        clearTimeout(timeout);
        timeout = null;
      }
      previous = now;
      result = func.apply(context, args);
      if (!timeout) {
        context = null;
        args = null;
      }
    } else if (!timeout && options.trailing !== false) {
      timeout = setTimeout(later, remaining);
    }
    return result;
  };
}

// js/context/duckdb.ts
async function initDuckdb() {
  const JSDELIVR_BUNDLES = getJsDelivrBundles();
  const bundle = await selectBundle(JSDELIVR_BUNDLES);
  const worker_url = URL.createObjectURL(
    new Blob([`importScripts("${bundle.mainWorker}");`], {
      type: "text/javascript"
    })
  );
  const worker = new Worker(worker_url);
  const logger = new ConsoleLogger(LogLevel.WARNING);
  const db = new AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  URL.revokeObjectURL(worker_url);
  return { db, worker };
}
async function waitForTable(conn, table, { interval = 250 } = {}) {
  while (true) {
    try {
      const res = await conn.query(
        `SELECT 1
           FROM information_schema.tables
         WHERE table_schema = 'main'
           AND table_name   = '${table}'
         LIMIT 1`
      );
      if (res.numRows) return;
    } catch (err) {
      console.log(
        `Table ${table} not yet available, trying again in ${interval}ms (error: ${err})`
      );
    }
    await sleep(interval);
  }
}

// js/util/errors.ts
function initializeErrorHandling(ctx, worker) {
  window.addEventListener("error", (event) => {
    ctx.recordUnhandledError(errorInfo(event.error));
  });
  window.addEventListener("unhandledrejection", (event) => {
    ctx.recordUnhandledError(errorInfo(event.reason));
  });
  worker.addEventListener("message", (event) => {
    if (event.data.type === "ERROR") {
      ctx.recordUnhandledError(errorInfo(event.data.data.message));
    }
  });
}
function errorInfo(error) {
  if (isError(error)) {
    return {
      name: error.name || "Error",
      message: error.message || "An unknown error occurred",
      stack: error.stack || "",
      code: error.code || null,
      ...error
      // Include any custom properties
    };
  } else if (typeof error === "string") {
    return {
      name: "Error",
      message: error,
      stack: new Error().stack || "",
      code: null
    };
  } else {
    return {
      name: "Unknown Error",
      message: JSON.stringify(error, null, 2),
      stack: new Error().stack || "",
      code: null,
      originalValue: error
    };
  }
}
function errorAsHTML(error) {
  const colors = {
    bg: "#ffffff",
    border: "#dc3545",
    title: "#dc3545",
    text: "#212529",
    subtext: "#6c757d",
    codeBg: "#f8f9fa",
    link: "#007bff"
  };
  const stackLines = parseStackTrace(error.stack);
  let html = `
    <div style="
      background: ${colors.bg};
      border: 2px solid ${colors.border};
      border-radius: 8px;
      padding: 20px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;
      color: ${colors.text};
      margin: 10px 0;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      width: 100%;
    ">
      <div style="display: flex; align-items: center; margin-bottom: 15px;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-right: 10px;">
          <circle cx="12" cy="12" r="10" stroke="${colors.title}" stroke-width="2" fill="none"/>
          <path d="M12 8v5m0 4h.01" stroke="${colors.title}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h3 style="margin: 0; color: ${colors.title}; font-size: 20px; font-weight: 600;">
          ${escapeHtml(error.name)}
        </h3>
      </div>
      
      <div style="
        background: ${colors.codeBg};
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
        border-left: 4px solid ${colors.border};
      ">
        <p style="margin: 0; font-size: 13px; line-height: 1.5; font-family: monospace; white-space: pre-wrap;">${escapeHtml(error.message)}</p>
      </div>`;
  if (error.code !== null) {
    html += `
      <div style="margin-bottom: 10px;">
        <span style="color: ${colors.subtext}; font-size: 143x;">Error Code:</span>
        <span style="color: ${colors.text}; font-weight: 500; margin-left: 8px;">
          ${escapeHtml(String(error.code))}
        </span>
      </div>`;
  }
  if (stackLines.length > 0) {
    html += `
      <details style="margin-top: 15px;">
        <summary style="
          cursor: pointer;
          color: ${colors.subtext};
          font-size: 13px;
          font-weight: 500;
          outline: none;
          user-select: none;
        ">
          Stack Trace (${stackLines.length} frames)
        </summary>
        <div style="margin-top: 10px; font-size: 13px; font-family: monospace;">`;
    stackLines.forEach((line, i) => {
      html += `
        <div style="
          background: ${i % 2 === 0 ? colors.codeBg : "transparent"};
          border-radius: 4px;
          margin: 2px 0;
          display: flex;
          align-items: center;
        ">
          <span style="color: ${colors.subtext}; min-width: 24px;">${i + 1}.</span>
          <span style="color: ${colors.link}; margin-left: 8px;">
            ${escapeHtml(line)}
          </span>
        </div>`;
    });
    html += `
        </div>
      </details>`;
  }
  html += `</div>`;
  return html;
}
function displayRenderError(error, renderEl) {
  renderEl.setAttribute("style", "");
  renderEl.innerHTML = errorAsHTML(error);
}
function parseStackTrace(stack) {
  if (!stack) return [];
  const lines = stack.split("\n");
  const functions = [];
  const patterns = [
    // Chrome/Edge: "    at functionName (file:line:column)"
    /^\s*at\s+(.+?)\s+\(/,
    // Chrome/Edge: "    at file:line:column" (anonymous)
    /^\s*at\s+[^(]+$/,
    // Firefox/Safari: "functionName@file:line:column"
    /^(.+?)@/
  ];
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed === "Error") continue;
    let functionName = "anonymous";
    for (const pattern of patterns) {
      const match = trimmed.match(pattern);
      if (match) {
        if (match[1]) {
          functionName = match[1].trim();
        }
        break;
      }
    }
    if (functionName === "anonymous" && !patterns.some((p) => p.test(trimmed))) {
      functionName = trimmed;
    }
    functions.push(functionName);
  }
  return functions;
}
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
function isError(value) {
  return value instanceof Error;
}

// js/context/index.ts
var VizContext = class extends InstantiateContext {
  constructor(conn_, plotDefaults) {
    super({ plotDefaults });
    this.conn_ = conn_;
    this.api = { ...this.api, ...INPUTS };
    this.coordinator.databaseConnector(wasmConnector({ connection: this.conn_ }));
  }
  tables_ = /* @__PURE__ */ new Set();
  unhandledErrors_ = [];
  async insertTable(table, data) {
    if (this.tables_.has(table)) {
      await this.waitForTable(table);
      return;
    }
    this.tables_.add(table);
    await this.conn_?.insertArrowFromIPCStream(data, {
      name: table,
      create: true
    });
  }
  async waitForTable(table) {
    await waitForTable(this.conn_, table);
  }
  recordUnhandledError(error) {
    this.unhandledErrors_.push(error);
  }
  async collectUnhandledError(wait = 1e3) {
    const startTime = Date.now();
    while (Date.now() - startTime < wait) {
      if (this.unhandledErrors_.length > 0) {
        return this.unhandledErrors_.shift();
      }
      await sleep(100);
    }
    return void 0;
  }
  clearUnhandledErrors() {
    this.unhandledErrors_ = [];
  }
};
var VIZ_CONTEXT_KEY = Symbol.for("@@inspect-viz-context");
async function vizContext(plotDefaults) {
  const globalScope = typeof window !== "undefined" ? window : globalThis;
  if (!globalScope[VIZ_CONTEXT_KEY]) {
    globalScope[VIZ_CONTEXT_KEY] = (async () => {
      const { db, worker } = await initDuckdb();
      const conn = await db.connect();
      const ctx = new VizContext(conn, plotDefaults);
      initializeErrorHandling(ctx, worker);
      return ctx;
    })();
  }
  return globalScope[VIZ_CONTEXT_KEY];
}

// js/util/platform.ts
function isNotebook() {
  const win = window;
  const hasNotebookGlobal = typeof win.Jupyter !== "undefined" || typeof win._JUPYTERLAB !== "undefined" || typeof win.google !== "undefined" && win.google.colab || typeof win.IPython !== "undefined" || typeof win.mo !== "undefined" || typeof win.acquireVsCodeApi !== "undefined";
  return hasNotebookGlobal || isVSCodeNotebook();
}
function isVSCodeNotebook() {
  return window.location.protocol === "vscode-webview:" && window.location.search.includes("purpose=notebookRenderer");
}

// js/plot/tooltips.ts
import svgPathParser from "https://cdn.jsdelivr.net/npm/svg-path-parser@1.1.0/+esm";
import tippy from "https://cdn.jsdelivr.net/npm/tippy.js@6.3.7/+esm";

// js/util/url.ts
var isUrl = (value) => {
  try {
    new URL(value);
    return true;
  } catch (e) {
    return false;
  }
};
var isLinkableUrl = (value) => {
  return isUrl(value) && value.startsWith("http");
};

// js/plot/plot.ts
var readMarks = (plotEl) => {
  const value = plotEl.value;
  const marks = value ? value.marks || [] : [];
  return marks;
};
var readOptions = (el) => {
  const value = el.value;
  return value ? value.options || {} : {};
};
var readPlotEl = (el) => {
  const value = el.value;
  const plot = value?.plot;
  if (plot) {
    return plot.element;
  }
  return void 0;
};
var hasValue = (el, key) => {
  const value = el.value;
  return value ? !!value[key] || false : false;
};

// js/plot/tooltips.ts
var HIDDEN_USER_CHANNEL = "_user_channels";
var replaceTooltipImpl = (specEl) => {
  configureSpecSvgTooltips(specEl);
  const observer = new MutationObserver(() => {
    configureSpecSvgTooltips(specEl);
  });
  observer.observe(specEl, { childList: true, subtree: true });
};
var configuredSvgs = /* @__PURE__ */ new WeakSet();
var configureSpecSvgTooltips = (specEl) => {
  const childSvgEls = specEl.querySelectorAll("svg");
  childSvgEls.forEach((svgEl) => {
    if (svgEl && !configuredSvgs.has(svgEl)) {
      setupTooltipObserver(svgEl, specEl);
      configuredSvgs.add(svgEl);
      return;
    }
  });
};
var tooltipInstance = void 0;
var tooltipSpecEl = void 0;
function initializeTooltip(specEl) {
  if (!tooltipInstance || tooltipSpecEl !== specEl) {
    if (tooltipInstance) {
      tooltipInstance.destroy();
    }
    tooltipInstance = tippy(specEl, {
      trigger: "manual",
      theme: "inspect",
      interactive: true
    });
    tooltipSpecEl = specEl;
  }
}
function hideTooltip() {
  try {
    tooltipInstance.hide();
  } catch {
  } finally {
    window.removeEventListener("scroll", hideTooltip);
  }
}
function maybeHideTooltip() {
  if (!tooltipInstance.popper.matches(":hover")) {
    hideTooltip();
  }
}
function showTooltip() {
  try {
    tooltipInstance.show();
    window.addEventListener("scroll", hideTooltip, { once: true });
  } catch {
  }
}
var setupTooltipObserver = (svgEl, specEl) => {
  initializeTooltip(specEl);
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === "childList") {
        const tipElements = svgEl.querySelectorAll('g[aria-label="tip"]');
        for (const tipElement of tipElements) {
          const tipContainerEl2 = tipElement;
          tipContainerEl2.style.display = "none";
        }
        let tipEl = void 0;
        let tipContainerEl = void 0;
        for (const tipElement of tipElements) {
          const searchElement = tipElement;
          const pathEl = searchElement.querySelector("path");
          const pathElParent = pathEl?.parentElement;
          if (pathElParent) {
            tipEl = pathElParent;
            tipContainerEl = searchElement;
            break;
          }
        }
        if (!tipEl || !tipContainerEl) {
          maybeHideTooltip();
        } else {
          const userChannels = readUserChannels(svgEl);
          const userKeys = userChannels ? Object.keys(userChannels) : void 0;
          const parsed = parseSVGTooltip(tipContainerEl, tipEl);
          const tooltips = distillTooltips(parsed, userKeys);
          const svgPoint = svgEl.createSVGPoint();
          svgPoint.x = parsed.transform?.x || 0;
          svgPoint.y = parsed.transform?.y || 0;
          const screenPoint = svgPoint.matrixTransform(svgEl.getScreenCTM());
          const centerX = screenPoint.x;
          const centerY = screenPoint.y;
          tooltipInstance.setProps({
            placement: parsed.placement !== "middle" ? parsed.placement || "top" : "top",
            getReferenceClientRect: () => {
              return {
                width: 0,
                height: 0,
                top: centerY,
                bottom: centerY,
                left: centerX,
                right: centerX,
                x: centerX,
                y: centerY,
                toJSON: () => {
                }
              };
            },
            arrow: parsed.placement !== "middle",
            offset: parsed.placement === "middle" ? [0, 0] : void 0,
            popperOptions: (
              // Special handling for middle placement, which isn't a supported
              // tippy placement
              parsed.placement === "middle" ? {
                modifiers: [
                  {
                    name: "preventOverflow",
                    enabled: false
                  },
                  {
                    name: "flip",
                    enabled: false
                  },
                  {
                    name: "customMiddle",
                    enabled: true,
                    phase: "main",
                    fn: ({ state }) => {
                      state.modifiersData.popperOffsets.x = centerX - state.rects.popper.width / 2;
                      state.modifiersData.popperOffsets.y = centerY - state.rects.popper.height / 2;
                    }
                  }
                ]
              } : void 0
            )
          });
          const contentEl = document.createElement("div");
          contentEl.classList.add("inspect-tip-container");
          let count2 = 0;
          for (const row of tooltips) {
            const rowEl = document.createElement("div");
            rowEl.className = "inspect-tip-row";
            contentEl.appendChild(rowEl);
            const keyEl = document.createElement("div");
            keyEl.className = "inspect-tip-key";
            keyEl.append(document.createTextNode(row.key));
            const valueEl = document.createElement("div");
            valueEl.className = "inspect-tip-value";
            if (row.href) {
              const linkEl = document.createElement("a");
              linkEl.href = row.href;
              linkEl.target = "_blank";
              linkEl.rel = "noopener noreferrer";
              linkEl.className = "inspect-tip-link";
              linkEl.textContent = row.value;
              valueEl.appendChild(linkEl);
            } else {
              valueEl.append(document.createTextNode(row.value));
            }
            if (row.color) {
              const colorEl = document.createElement("span");
              colorEl.className = "inspect-tip-color";
              colorEl.style.backgroundColor = row.color;
              valueEl.append(colorEl);
            }
            rowEl.appendChild(keyEl);
            rowEl.appendChild(valueEl);
            count2++;
          }
          tooltipInstance.setContent(contentEl);
          showTooltip();
        }
      }
    });
  });
  observer.observe(svgEl, {
    childList: true,
    subtree: true
  });
};
var parseTransform = (el) => {
  const transformVal = el.getAttribute("transform");
  if (transformVal) {
    const match = transformVal.match(/translate\(([^)]+)\)/);
    if (match) {
      const [x, y] = match[1].split(",").map(Number);
      return { x, y };
    }
  }
  return void 0;
};
var parseSVGTooltip = (tipContainerEl, tipEl) => {
  const result = { values: [] };
  const tspanEls = tipEl.querySelectorAll("tspan");
  tspanEls.forEach((tspan) => {
    let key = void 0;
    let value = void 0;
    let color = void 0;
    tspan.childNodes.forEach((node) => {
      if (node.nodeName === "tspan") {
        const colorAttr = node.getAttribute("fill");
        if (colorAttr) {
          color = colorAttr;
        } else {
          key = node.textContent?.trim();
        }
      } else if (node.nodeName === "#text") {
        value = node.textContent?.trim();
      }
    });
    if (key !== void 0 && value !== void 0) {
      if (isLinkableUrl(value)) {
        result.values.push({ key, value: "Link", href: value, color });
      } else {
        result.values.push({ key, value, color });
      }
    }
  });
  const pathEl = tipEl.querySelector("path");
  if (pathEl) {
    const pathData = pathEl.getAttribute("d");
    if (pathData) {
      result.placement = parseArrowDirection(pathData);
    }
    const transforms = getTransformsBetween(pathEl, tipContainerEl);
    if (transforms.length > 0) {
      result.transform = transforms.reduce(
        (acc, transform) => {
          acc.x += transform.x;
          acc.y += transform.y;
          return acc;
        },
        { x: 0, y: 0 }
      );
    }
  }
  return result;
};
function distillTooltips(parsed, userKeys) {
  if (!userKeys) {
    return parsed.values;
  }
  const userValues = parsed.values.filter((row) => {
    return userKeys.includes(row.key);
  }).map((row) => row.value);
  const filteredRows = parsed.values.filter((row) => {
    if (row.key === HIDDEN_USER_CHANNEL) {
      return false;
    }
    if (row.key.startsWith("_")) {
      return false;
    }
    if (userKeys.includes(row.key)) {
      return true;
    }
    if (userValues.includes(row.value)) {
      return false;
    }
    return false;
  });
  return filteredRows;
}
function readUserChannels(svgEl) {
  const plotEl = svgEl.parentElement;
  if (plotEl) {
    const marks = readMarks(plotEl);
    for (const mark of marks) {
      const markChannels = mark.channels || [];
      const markChannelNames = markChannels.map((c) => c.channel);
      if (markChannelNames.includes("tip")) {
        const userChannels = markChannels.find(
          (c) => c.channel === HIDDEN_USER_CHANNEL
        );
        const userChannelsValue = userChannels?.value;
        if (userChannelsValue) {
          const parsedChannels = JSON.parse(userChannelsValue);
          return parsedChannels;
        }
      }
    }
  }
  return void 0;
}
function getTransformsBetween(pathElement, containerElement) {
  const transforms = [];
  let current = pathElement.parentElement;
  while (current) {
    const transform = parseTransform(current);
    if (transform) {
      transforms.unshift(transform);
    }
    if (current !== containerElement) {
      current = current.parentElement;
    } else {
      break;
    }
  }
  return transforms;
}
var parseArrowPosition = (a, b) => {
  if (a < b) {
    return "end";
  } else if (a > b) {
    return "start";
  } else {
    return "center";
  }
};
var parseArrowDirection = (pathData) => {
  const parsed = svgPathParser.parseSVG(pathData);
  if (parsed.length < 3) {
    return "top";
  }
  const moveTo = parsed[0];
  if (moveTo.code !== "M") {
    console.warn("Expected moveto command (M) in path data, found:", moveTo);
    return "top";
  }
  if (moveTo.x !== 0 && moveTo.y !== 0) {
    return "middle";
  }
  const lineTo = parsed[1];
  if (lineTo.code !== "l") {
    console.warn("Expected lineto command (l) in path data, found:", lineTo);
    return "top";
  }
  const firstEdgeLineTo = parsed[2];
  if (firstEdgeLineTo.code !== "h" && firstEdgeLineTo.code !== "v") {
    console.warn(
      "Expected horizontal (h) or vertical (v) line command after move, found:",
      firstEdgeLineTo
    );
    return "top";
  }
  const lastEdgeLineTo = parsed[parsed.length - 2];
  if (lastEdgeLineTo.code !== "h" && lastEdgeLineTo.code !== "v") {
    console.warn(
      "Expected horizontal (h) or vertical (v) line command before close, found:",
      lastEdgeLineTo
    );
    return "top";
  }
  const x = lineTo.x;
  const y = lineTo.y;
  let arrowDirection = "top";
  if (x > 0 && y > 0) {
    arrowDirection = "bottom";
  } else if (x < 0 && y < 0) {
    if (firstEdgeLineTo.code === "h") {
      arrowDirection = "bottom";
    } else {
      arrowDirection = "left";
    }
  } else if (x > 0 && y < 0) {
    if (firstEdgeLineTo.code === "h") {
      arrowDirection = "top";
    } else {
      arrowDirection = "right";
    }
  } else if (x < 0 && y > 0) {
    arrowDirection = "bottom";
  } else {
    console.warn(
      "Could not determine arrow direction from path data, returning default placement: top"
    );
  }
  let arrowPosition = "center";
  if (firstEdgeLineTo.code === "h") {
    arrowPosition = parseArrowPosition(firstEdgeLineTo.x, lastEdgeLineTo.x);
  } else {
    arrowPosition = parseArrowPosition(firstEdgeLineTo.y, lastEdgeLineTo.y);
  }
  if (arrowPosition === "center") {
    return arrowDirection;
  } else {
    return `${arrowDirection}-${arrowPosition}`;
  }
};

// js/plot/text-collision.ts
import * as d3 from "https://cdn.jsdelivr.net/npm/d3-force@3.0.0/+esm";
var installTextCollisionHandler = (specEl) => {
  configurePlotObservers(specEl);
  const observer = new MutationObserver(() => {
    configurePlotObservers(specEl);
  });
  observer.observe(specEl, { childList: true, subtree: true });
};
var configuredPlots = /* @__PURE__ */ new WeakSet();
var configurePlotObservers = (specEl) => {
  const childSvgEls = specEl.querySelectorAll("div.plot svg");
  childSvgEls.forEach((svgEl) => {
    if (svgEl && !configuredPlots.has(svgEl)) {
      const options = readTextOptions(svgEl);
      if (options.shiftOverlappingText) {
        configurePlotObserver(svgEl);
        configuredPlots.add(svgEl);
      }
    }
  });
};
var configurePlotObserver = (plotElement) => {
  const observer = new MutationObserver(() => {
    processCollidingText(plotElement);
  });
  processCollidingText(plotElement);
  observer.observe(plotElement, { childList: true, subtree: true });
};
function processCollidingText(plotElement) {
  const textElements = plotElement.querySelectorAll('g[aria-label="text"] text');
  if (textElements.length === 0) {
    return;
  }
  const nodes = Array.from(textElements).map((el) => {
    const textEl = el;
    const screenRect = textEl.getBoundingClientRect();
    const svgRect = plotElement.getBoundingClientRect();
    const actualX = screenRect.left - svgRect.left + screenRect.width / 2;
    const actualY = screenRect.top - svgRect.top + screenRect.height / 2;
    const originalSvgX = parseFloat(textEl.getAttribute("x") || "0");
    const originalSvgY = parseFloat(textEl.getAttribute("y") || "0");
    return {
      element: textEl,
      rect: screenRect,
      x: actualX,
      y: actualY,
      initialX: actualX,
      initialY: actualY,
      originalSvgX,
      originalSvgY
    };
  });
  d3.forceSimulation(nodes).force("collision", rectangularVerticalCollisionForce().padding(0)).force("x", d3.forceX((d) => d.initialX).strength(0.1)).force("y", d3.forceY((d) => d.initialY).strength(0.1)).alphaDecay(0.75).velocityDecay(0.9).on("tick", () => {
    nodes.forEach((d) => {
      const deltaX = d.x - d.initialX;
      if (deltaX !== 0) {
        d.element.setAttribute("x", String(d.originalSvgX + deltaX));
      }
      const deltaY = d.y - d.initialY;
      if (deltaY !== 0) {
        d.element.setAttribute("y", String(d.originalSvgY + deltaY));
      }
    });
  });
}
function rectangularVerticalCollisionForce() {
  let nodes;
  let padding = 2;
  function force() {
    for (let i = 0; i < nodes.length; i++) {
      const nodeA = nodes[i];
      const rectA = nodeA.rect;
      for (let j = i + 1; j < nodes.length; j++) {
        const nodeB = nodes[j];
        const rectB = nodeB.rect;
        const aLeft = nodeA.x - rectA.width / 2;
        const aRight = nodeA.x + rectA.width / 2;
        const aTop = nodeA.y - rectA.height / 2;
        const aBottom = nodeA.y + rectA.height / 2;
        const bLeft = nodeB.x - rectB.width / 2;
        const bRight = nodeB.x + rectB.width / 2;
        const bTop = nodeB.y - rectB.height / 2;
        const bBottom = nodeB.y + rectB.height / 2;
        const xOverlap = aRight + padding > bLeft && bRight + padding > aLeft;
        const yOverlap = aBottom + padding > bTop && bBottom + padding > aTop;
        if (xOverlap && yOverlap) {
          const dy = nodeB.y - nodeA.y;
          const minDistanceY = (rectA.height + rectB.height) / 2 + padding;
          if (Math.abs(dy) < minDistanceY) {
            const overlapY = minDistanceY - Math.abs(dy);
            const moveY = overlapY / 2 * (dy > 0 ? 1 : -1);
            nodeA.y -= moveY;
            nodeB.y += moveY;
          }
        }
      }
    }
  }
  force.initialize = function(newNodes) {
    nodes = newNodes;
  };
  force.padding = function(value) {
    if (value === void 0) return padding;
    padding = value;
    return force;
  };
  return force;
}
var readTextOptions = (svgEl) => {
  const textOptions = {};
  const plotEl = svgEl.parentElement;
  if (plotEl) {
    const marks = readMarks(plotEl);
    const textMarks = marks.filter((mark) => mark.type === "text");
    for (const mark of textMarks) {
      const shiftTextEnabled = mark.channels?.some((c) => {
        if (c.channel === "_shift_overlapping_text") {
          const val = c.value;
          if (Array.isArray(val)) {
            return val.includes(true);
          }
        }
        return false;
      });
      if (shiftTextEnabled) {
        textOptions.shiftOverlappingText = true;
        break;
      }
    }
  }
  return textOptions;
};

// js/plot/ticks.ts
import * as d3TimeFormat2 from "https://cdn.jsdelivr.net/npm/d3-time-format@4.1.0/+esm";

// js/util/spec.ts
function visitPlot(obj, fn) {
  if (Array.isArray(obj)) {
    obj.flatMap((item) => visitPlot(item, fn));
  } else if (typeof obj === "object" && obj !== null) {
    if ("plot" in obj) {
      fn(obj);
    } else {
      Object.values(obj).flatMap((value) => visitPlot(value, fn));
    }
  }
}

// js/plot/ticks.ts
var applyTickFormatting = (spec) => {
  visitPlot(spec, (plot) => {
    if ("xTickFormat" in plot) {
      const format2 = plot.xTickFormat;
      if (typeof format2 === "string") {
        processTickFormat(plot, "xTickFormat");
        processTickFormat(plot, "yTickFormat");
      }
    }
  });
};
var processTickFormat = (obj, formatKey) => {
  if (formatKey in obj) {
    const format2 = obj[formatKey];
    if (typeof format2 === "string") {
      if (isD3TimeFormat(format2)) {
        obj[formatKey] = (val) => {
          if (typeof val === "number") {
            const d = new Date(val);
            return d3TimeFormat2.timeFormat(format2)(d);
          } else {
            return d3TimeFormat2.timeFormat(format2)(val);
          }
        };
      }
    }
  }
};
var isD3TimeFormat = (format2) => {
  return /%[aAbBcdefHIjLmMpqQsSuUVwWxXyYzZ%]/.test(format2);
};

// js/plot/legend.ts
var kInsetX = "_inset_x";
var kInsetY = "_inset_y";
var kInset = "_inset";
var kFrameAnchor = "_frame_anchor";
var kBackground = "_background";
var kBorder = "_border";
var installLegendHandler = (specEl, responsive) => {
  const existingObserver = observedSpecs.get(specEl);
  if (existingObserver) {
    existingObserver.disconnect();
    observedSpecs.delete(specEl);
  }
  const hasLegend = specEl.querySelector("div.legend") !== null;
  if (!hasLegend) {
    return;
  }
  configureLegendHandler(specEl, responsive);
  const observer = new MutationObserver(() => {
    configureLegendHandler(specEl, responsive);
  });
  observer.observe(specEl, { childList: true, subtree: true });
  observedSpecs.set(specEl, observer);
};
var observedSpecs = /* @__PURE__ */ new WeakMap();
function legendPaddingRegion(spec) {
  const result = { top: false, bottom: false, left: false, right: false };
  function visitLegends(obj) {
    if (!obj || typeof obj !== "object") return;
    if ("legend" in obj) {
      const legendObj = obj;
      const hasInset = kInset in legendObj || kInsetX in legendObj || kInsetY in legendObj;
      if (!hasInset && kFrameAnchor in legendObj) {
        const frameAnchor = legendObj[kFrameAnchor];
        switch (frameAnchor) {
          case "top":
          case "top-left":
          case "top-right":
            result.top = true;
            break;
          case "bottom":
          case "bottom-left":
          case "bottom-right":
            result.bottom = true;
            break;
          case "left":
            result.left = true;
            break;
          case "right":
            result.right = true;
            break;
        }
      }
    }
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        visitLegends(obj[key]);
      }
    }
    if (Array.isArray(obj)) {
      obj.forEach((item) => visitLegends(item));
    }
  }
  visitLegends(spec);
  return result;
}
var configuredLegends = /* @__PURE__ */ new WeakSet();
var specHandlers = /* @__PURE__ */ new WeakMap();
var configureLegendHandler = (specEl, responsive) => {
  const newLegends = Array.from(specEl.querySelectorAll("div.legend")).filter(
    (legend) => !configuredLegends.has(legend)
  );
  if (newLegends.every((legend) => legend.childElementCount === 0)) {
    return;
  }
  const frameLegends = groupLegendsByPosition(newLegends);
  const existingObserver = specHandlers.get(specEl);
  if (existingObserver) {
    existingObserver.disconnect();
    specHandlers.delete(specEl);
  }
  const processLegends = throttle2(() => {
    const legends = specEl.querySelectorAll("div.legend");
    legends.forEach((legend) => {
      const legendEl = legend;
      applyLegendStyles(legendEl);
    });
  }, 25);
  if (newLegends.length > 0) {
    emplaceLegendContainers(frameLegends, specEl);
    newLegends.forEach((legend) => configuredLegends.add(legend));
  }
  processLegends();
  if (responsive) {
    const observer = new ResizeObserver(() => {
      processLegends();
    });
    observer.observe(specEl);
    specHandlers.set(specEl, observer);
  }
};
var applyLegendStyles = (legendEl) => {
  const options = readLegendOptions(legendEl);
  if (!options.frameAnchor) {
    return;
  }
  const legendContainerEl = legendEl.parentElement;
  const legendContainerParentEl = legendContainerEl.parentElement;
  legendContainerParentEl.style.position = "relative";
  if (options.frameAnchor === "bottom" || options.frameAnchor === "top") {
    legendContainerEl.style.padding = "0 0.3em";
  } else {
    legendContainerEl.style.padding = "0.3em";
  }
  legendContainerEl.style.width = "max-content";
  applyBackground(legendContainerEl, options.background);
  applyBorder(legendContainerEl, options.border);
  applyParentPadding(options, legendContainerEl, legendContainerParentEl);
  responsiveScaleLegend(options, legendEl, legendContainerEl);
  applyCursorStyle(legendEl);
};
var applyBackground = (targetEl, background) => {
  if (background !== false) {
    const backgroundDefaultColor = "var(--bs-body-bg, var(--jp-cell-editor-background, #ffffff))";
    targetEl.style.background = background === true ? backgroundDefaultColor : background || backgroundDefaultColor;
  }
};
var applyBorder = (targetEl, border) => {
  if (border !== false) {
    const borderColor = border === true ? "#DDDDDD" : border || "#DDDDDD";
    targetEl.style.border = `1px solid ${borderColor}`;
  }
};
var applyCursorStyle = (legendEl) => {
  const existingObserver = cursorObserver.get(legendEl);
  if (existingObserver) {
    existingObserver.disconnect();
    cursorObserver.delete(legendEl);
  }
  const applyPointer = () => {
    if (hasValue(legendEl, "selection")) {
      const subContainerEl = legendEl.firstElementChild;
      subContainerEl.style.cursor = "pointer";
    }
  };
  const observer = new MutationObserver(() => {
    applyPointer();
  });
  observer.observe(legendEl, { childList: true, subtree: true });
  applyPointer();
  cursorObserver.set(legendEl, observer);
};
var cursorObserver = /* @__PURE__ */ new WeakMap();
var applyParentPadding = (options, legendEl, parentEl) => {
  if (!options.inset) {
    const observer = new MutationObserver(() => {
      if (options.frameAnchor) {
        const newSize = legendEl.getBoundingClientRect();
        const parentConfig = kParentAnchorConfig[options.frameAnchor];
        const useHeight = parentConfig.paddingType === "paddingTop" || parentConfig.paddingType === "paddingBottom";
        parentEl.style[parentConfig.paddingType] = useHeight ? newSize.height + "px" : newSize.width + "px";
      }
    });
    observer.observe(legendEl, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["style", "class"]
    });
  }
};
var responsiveScaleLegend = (options, legendEl, legendContainerEl) => {
  const anchor = options.frameAnchor || "right";
  const config = getAnchorConfig(anchor, options);
  Object.assign(legendContainerEl.style, config.position);
  if (config.centerTransform) {
    legendContainerEl.style.transform = "translateX(-50%)";
  }
  const plotEl = readPlotEl(legendEl);
  if (!plotEl || !plotEl.children || plotEl.childElementCount === 0) {
    return;
  }
  const parentEl = plotEl.parentElement;
  if (!parentEl) {
    console.warn("No parent element found for the plot.");
    return;
  }
  const svgEl = plotEl.children[0];
  if (svgEl.tagName !== "svg") {
    console.warn("The first child of the plot element is not an SVG element.");
    return;
  }
  const baseWidth = svgEl.getAttribute("width");
  if (!baseWidth) {
    console.warn("Plot element does not have a width attribute.");
    return;
  }
  const parentRect = parentEl.getBoundingClientRect();
  const svgWidth = svgEl.getBoundingClientRect().width;
  const rawScaleFactor = svgWidth / parseFloat(baseWidth);
  const scaleFactor = Math.min(1, rawScaleFactor);
  const styles = {};
  if (config.transformOrigin) {
    styles.transformOrigin = config.transformOrigin;
  }
  if (config.centerTransform) {
    styles.transform = `translateX(-50%) scale(${scaleFactor})`;
  } else {
    styles.transform = `scale(${scaleFactor})`;
  }
  if (options.inset) {
    const plotRect = findPlotRegionRect(plotEl);
    const yShift = config.transformOrigin?.startsWith("bottom") ? parentRect.bottom - plotRect.bottom : plotRect.top - parentRect.top;
    const xShift = config.transformOrigin?.endsWith("right") ? parentRect.right - plotRect.right : plotRect.left - parentRect.left;
    const yInset = options.inset[1] * scaleFactor + yShift;
    const xInset = options.inset[0] * scaleFactor + xShift;
    if (config.centerTransform) {
      styles.margin = `${yInset}px 0px`;
    } else {
      styles.margin = `${yInset}px ${xInset}px`;
    }
  }
  Object.assign(legendContainerEl.style, styles);
};
var resolveOptions = (options) => {
  if (options.inset == null && options.insetX == null && options.insetY == null) {
    return {
      inset: void 0,
      frameAnchor: options.frameAnchor,
      background: options.background,
      border: options.border
    };
  }
  let inset = void 0;
  if (options.inset !== null && options.insetX === null && options.insetY === null) {
    inset = [Math.abs(options.inset), Math.abs(options.inset)];
  } else if (options.insetX !== null || options.insetY !== null) {
    inset = [Math.abs(options.insetX || 0), Math.abs(options.insetY || 0)];
  }
  return {
    inset,
    frameAnchor: options.frameAnchor,
    background: options.background,
    border: options.border
  };
};
var readLegendOptions = (legendEl) => {
  const optionsRaw = readOptions(legendEl);
  const options = {
    inset: optionsRaw[kInset],
    insetX: optionsRaw[kInsetX],
    insetY: optionsRaw[kInsetY],
    frameAnchor: optionsRaw[kFrameAnchor],
    background: optionsRaw[kBackground],
    border: optionsRaw[kBorder]
  };
  return resolveOptions(options);
};
var findPlotRegionRect = (plotEl) => {
  const plotRect = plotEl.getBoundingClientRect();
  const yLabel = plotEl.querySelector('g[aria-label="y-axis label"]');
  const top = yLabel ? yLabel.getBoundingClientRect().bottom : plotRect.top;
  const yTicks = plotEl.querySelector('g[aria-label="y-axis tick"]');
  const left = yTicks ? yTicks.getBoundingClientRect().right : plotRect.left;
  const right = plotRect.right;
  let bottom = plotRect.bottom;
  const xTicks = plotEl.querySelector('g[aria-label="x-axis tick"]');
  if (xTicks) {
    const xRect = xTicks.getBoundingClientRect();
    bottom = xRect.top;
  } else {
    const xLabel = plotEl.querySelector('g[aria-label="x-axis label"]');
    if (xLabel) {
      bottom = xLabel.getBoundingClientRect().top;
    }
  }
  return new DOMRect(left, top, right - left, bottom - top);
};
var kParentAnchorConfig = {
  "top-left": { paddingType: "paddingLeft" },
  top: { paddingType: "paddingTop" },
  "top-right": { paddingType: "paddingRight" },
  right: { paddingType: "paddingRight" },
  "bottom-right": { paddingType: "paddingRight" },
  bottom: { paddingType: "paddingBottom" },
  "bottom-left": { paddingType: "paddingLeft" },
  left: { paddingType: "paddingLeft" },
  middle: { paddingType: "" }
};
var getAnchorConfig = (anchor, options) => {
  switch (anchor) {
    case "top-left":
      return {
        position: { position: "absolute", top: "0", left: "0" },
        transformOrigin: "top left"
      };
    case "top":
      return {
        position: { position: "absolute", top: "0", left: "50%" },
        centerTransform: true,
        transformOrigin: "top center"
      };
    case "top-right":
      return {
        position: { position: "absolute", top: "0", right: "0" },
        transformOrigin: "top right"
      };
    case "right":
      if (options.inset) {
        return { position: { position: "absolute", right: "0" } };
      } else {
        return { position: {} };
      }
    case "bottom-right":
      return {
        position: { position: "absolute", bottom: "0", right: "0" },
        transformOrigin: "bottom right"
      };
    case "bottom":
      return {
        position: { position: "absolute", bottom: "0", left: "50%" },
        centerTransform: true,
        transformOrigin: "bottom center"
      };
    case "bottom-left":
      return {
        position: { position: "absolute", bottom: "0", left: "0" },
        transformOrigin: "bottom left"
      };
    case "left":
      return {
        position: { position: "absolute", left: "0" },
        transformOrigin: "center left"
      };
    case "middle":
      return { position: { position: "absolute" } };
  }
  return { position: { position: "absolute" } };
};
function emplaceLegendContainers(frameLegends, specEl) {
  for (const [positionKey, legendEls] of Object.entries(frameLegends)) {
    for (const legendEl of legendEls) {
      let containerEl = specEl.querySelector(
        `div.legend-container.${positionKey}`
      );
      if (containerEl === null) {
        containerEl = document.createElement("div");
        containerEl.className = `legend-container ${positionKey}`;
        legendEl.parentElement.insertBefore(containerEl, legendEl);
      }
      containerEl.appendChild(legendEl);
    }
  }
}
function groupLegendsByPosition(legends) {
  const frameLegends = {};
  for (const legend of Array.from(legends)) {
    const legendEl = legend;
    const options = readLegendOptions(legendEl);
    const legendKey = `${options.frameAnchor}-${options.inset?.[0] || 0}-${options.inset?.[1] || 0}`;
    frameLegends[legendKey] = frameLegends[legendKey] || [];
    frameLegends[legendKey].push(legendEl);
  }
  return frameLegends;
}

// js/widgets/mosaic.ts
async function render({ model, el }) {
  const spec = JSON.parse(model.get("spec"));
  const plotDefaultsSpec = { plotDefaults: spec.plotDefaults, vspace: 0 };
  const plotDefaultsAst = parseSpec(plotDefaultsSpec);
  const ctx = await vizContext(plotDefaultsAst.plotDefaults);
  applyTickFormatting(spec);
  const tables = model.get("tables") || {};
  await syncTables(ctx, tables);
  el.classList.add("mosaic-widget");
  const renderOptions = renderSetup(el);
  const inputs = new Set(Object.keys(INPUTS));
  if (renderOptions.autoFillScrolling && isPlotSpec(spec)) {
    el.style.width = "100%";
    el.style.height = "400px";
  }
  if (renderOptions.autoFill && isTableSpec(spec)) {
    const card = el.closest(".card-body");
    if (card) {
      card.style.padding = "0";
    }
  }
  const renderSpec = async () => {
    try {
      ctx.clearUnhandledErrors();
      const targetSpec = renderOptions.autoFill ? responsiveSpec(spec, el) : spec;
      const ast = parseSpec(targetSpec, { inputs });
      const specEl = await astToDOM(ast, ctx);
      el.innerHTML = "";
      el.appendChild(specEl);
      replaceTooltipImpl(specEl);
      installTextCollisionHandler(specEl);
      installLegendHandler(specEl, !renderOptions.autoFill);
      await displayUnhandledErrors(ctx, el);
    } catch (e) {
      console.error(e);
      const error = errorInfo(e);
      el.innerHTML = errorAsHTML(error);
    }
  };
  await renderSpec();
  if (renderOptions.autoFill && !isInputSpec(spec)) {
    let lastContainerWidth = el.clientWidth;
    let lastContainerHeight = el.clientHeight;
    const resizeObserver = new ResizeObserver(
      throttle3(async () => {
        if (lastContainerWidth !== el.clientWidth || lastContainerHeight !== el.clientHeight) {
          lastContainerWidth = el.clientWidth;
          lastContainerHeight = el.clientHeight;
          renderSpec();
        }
      })
    );
    resizeObserver.observe(el);
    return () => {
      resizeObserver.disconnect();
    };
  }
}
async function syncTables(ctx, tables) {
  for (const [tableName, base64Data] of Object.entries(tables)) {
    if (base64Data) {
      const binaryString = atob(base64Data);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      await ctx.insertTable(tableName, bytes);
    } else {
      await ctx.waitForTable(tableName);
    }
  }
}
function renderSetup(containerEl) {
  const widgetEl = containerEl.closest(".widget-subarea");
  if (widgetEl) {
    widgetEl.style.marginBottom = "0";
  }
  const autoFill = window.document.body.classList.contains("quarto-dashboard");
  const autoFillScrolling = autoFill && !window.document.body.classList.contains("dashboard-fill");
  return { autoFill, autoFillScrolling };
}
function responsiveSpec(spec, containerEl) {
  const kLegendWidth = 80;
  const kLegendHeight = 35;
  const paddingRegion = legendPaddingRegion(spec);
  const horizontalPadding = paddingRegion.left || paddingRegion.right ? kLegendWidth : 0;
  const verticalPadding = paddingRegion.top || paddingRegion.bottom ? kLegendHeight : 0;
  spec = structuredClone(spec);
  if ("input" in spec && spec.input === "table") {
    const table = spec;
    table.auto_filling = true;
  } else if ("hconcat" in spec && spec.hconcat.length == 1) {
    const hconcat = spec.hconcat;
    const plot = "plot" in hconcat[0] ? hconcat[0] : null;
    if (plot) {
      plot.width = containerEl.clientWidth - (hconcat.length > 1 ? horizontalPadding : 0);
      plot.height = containerEl.clientHeight;
    }
  } else if ("hconcat" in spec && spec.hconcat.length == 2) {
    const hconcat = spec.hconcat;
    const plot = "plot" in hconcat[0] && "legend" in hconcat[1] ? hconcat[0] : "plot" in hconcat[1] && "legend" in hconcat[0] ? hconcat[1] : void 0;
    if (plot) {
      plot.width = containerEl.clientWidth - (spec.hconcat.length > 1 ? horizontalPadding : 0);
      plot.height = containerEl.clientHeight;
    }
  } else if ("vconcat" in spec && spec.vconcat.length == 2) {
    const vconcat = spec.vconcat;
    const plot = "plot" in vconcat[0] && "legend" in vconcat[1] ? vconcat[0] : "plot" in vconcat[1] && "legend" in vconcat[0] ? vconcat[1] : void 0;
    if (plot) {
      plot.width = containerEl.clientWidth;
      plot.height = containerEl.clientHeight - (spec.vconcat.length > 1 ? verticalPadding : 0);
    }
  }
  return spec;
}
function isPlotSpec(spec) {
  if ("plot" in spec) {
    return true;
  } else if ("input" in spec && spec.input === "table") {
    return true;
  } else if ("hconcat" in spec && spec.hconcat.length === 2 && ("plot" in spec.hconcat[0] || "plot" in spec.hconcat[1])) {
    return true;
  } else if ("vconcat" in spec && spec.vconcat.length === 2 && ("plot" in spec.vconcat[0] || "plot" in spec.vconcat[1])) {
    return true;
  } else {
    return false;
  }
}
function isInputSpec(spec) {
  return "input" in spec && spec.input !== "table";
}
function isTableSpec(spec) {
  return "input" in spec && spec.input === "table";
}
async function astToDOM(ast, ctx) {
  for (const [name, node] of Object.entries(ast.params)) {
    if (!ctx.activeParams.has(name) || isNotebook()) {
      const param = node.instantiate(ctx);
      ctx.activeParams.set(name, param);
    }
  }
  return ast.root.instantiate(ctx);
}
async function displayUnhandledErrors(ctx, widgetEl) {
  const emptyPlotDivs = widgetEl.querySelectorAll("div.plot:empty");
  for (const emptyDiv of emptyPlotDivs) {
    const error = await ctx.collectUnhandledError();
    if (error) {
      displayRenderError(error, emptyDiv);
    }
  }
}
var mosaic_default = { render };
export {
  mosaic_default as default
};
