#! /usr/bin/env hy
"""
    tqwgp-parser.parser
    ~~~~~~~~~~~~~~~~~~~~~
    Parse the definitions of TWWGP quotes and invoices.
    :copyright: (c) 2017-2021 Yoan Tournade.
"""
(import copy)
(import os)
(require [hy.extra.anaphoric [*]])

;; Utils.

(defn parse-dict-values [value mandatories optionals]
  ;; Use dict-comp http://docs.hylang.org/en/stable/language/api.html#dict-comp?
  (setv parsed-dict {})
  (for [key (.keys value)] ((fn [key]
    (if (or (in key mandatories) (in key optionals))
      (assoc parsed-dict key (get value key))
      (print (.format "Ignoring key {}" key)))) key))
  ;; Check all mandatories are here.
  (for [mandatory mandatories] ((fn [mandatory]
    (if (not (in mandatory parsed-dict))
      (raise (ValueError (.format "Missing key {}" mandatory))))) mandatory))
  ;; Affect None to non-set optionals.
  (for [optional optionals] ((fn [optional]
    (if (not (in optional parsed-dict))
      (assoc parsed-dict optional None))) optional))
  parsed-dict)

(defn merge-dicts [dicts]
  (setv merged (.deepcopy copy (get dicts 0)))
  (for [one-dict (drop 1 dicts)] ((fn [one-dict]
    (.update merged one-dict)) one-dict))
  merged)

(defn filter-dict [a-dict pred]
  (setv new-dict {})
  (ap-each (.keys a-dict)
    (if (pred (get a-dict it) it)
      (assoc new-dict it (get a-dict it))))
  new-dict)

(defn find-in-list [l pred]
  (setv element None)
  (for [item l] ((fn [item])
    (if (pred item)
      (do
        (setv element item)
        (break))) l))
  element)

(defn pred-has-entry-value [key value]
  (fn [element]
    (= (get element key) value)))

(defn get-default [value key default]
  (if (in key value)
    (get value key)
    default))

(defn pick-by [pred value]
  (setv new-value {})
  (for [key (.keys value)] ((fn [key]
    (if (pred key)
      (assoc new-value key (get value key)))) key))
  new-value)

(defn simplest-numerical-format [price]
  (if (.is_integer (float price))
    (int price)
    price))

(defn none-or-true? [value]
  (or (none? value) (bool value)))

;; Data parsing and normalization.

(defn parse-all-prestations [prestations &optional [section None]]
  """
  Parse all prestations, returning a flattened list of prestations (in all-prestations)
  and a list of sections.
  Prestation parsed refer to section by their id (title).
  Sections contain all their prestations.
  """
  (setv all-prestations [])
  (setv sections [])
  (for [prestation prestations] ((fn [prestation]
    (if (in "prestations" prestation)
      (do
        (setv section-prestations
          (get (parse-all-prestations (get prestation "prestations") prestation) 0))
        (.append sections (parse-section prestation section-prestations))
        (.extend all-prestations section-prestations))
      (.append all-prestations (parse-prestation prestation section))
    )) prestation))
  (, all-prestations sections))

(defn parse-prestation [prestation section]
  (merge-dicts [
    (parse-dict-values prestation
      ["title"]
      ["price" "quantity" "description" "batch" "optional"])
    {
      "quantity" (get-default prestation "quantity" 1)
      "section" (get-default (if (none? section) {} section) "title" None)
      "batch" (parse-batch (get-default prestation "batch" (get-default (if (none? section) {} section) "batch" None)))
      "optional" (get-default prestation "optional" (get-default (if (none? section) {} section) "optional" False))
    }]))

(defn parse-section [section prestations]
  (merge-dicts [
    (parse-dict-values section
      ["title" "prestations"]
      ["description" "batch"])
    {
      "prestations" prestations
      "price" (compute-price prestations :count-optional True)
      ;; TODO Normalize batch here: only set if all section prestation has same batch
      ;; (alternative: set a list of batches).
      "batch" (parse-batch (get-default section "batch" None))
      "optional" (get-default section "optional" False)
    }]))

(defn compute-price [prestations &optional [count-optional False]]
  """
  Parse price of a flattened list of prestations
  (actually any list with object containing a price property),
  with quantity support.
  """
  ;; Must accept (but ignore for total) None and string values.
  ;; Set to None if no price defined at all.
  (reduce
    (fn [total prestation]
      (setv price (get prestation "price"))
      (setv add-price (and (numeric? price) (or count-optional (not (get-default prestation "optional" False)))))
      (setv prestation-total (if (numeric? price) (* price (get-default prestation "quantity" 1))))
      (cond
        [(and add-price (numeric? total))
          (+ total prestation-total)]
        [add-price
          prestation-total]
        [True
          total]))
    prestations
    None))

(defn compute-vat [price vat-rate]
  """
  Compute VAT part on a numerical price.
  vat-rate is represented as an integer percent points value, for e.g. 20 for a 20 % VAT rate.
  """
  (simplest-numerical-format (* (/ vat-rate 100) price)))

(defn compute-price-vat [prestations &optional [count-optional False] [vat-rate None]]
  """
  Compute price, as an object including VAT component, total with VAT excluded, total with VAT included ;
  from a list of objects containing a price (numerical) property.
  """
  ;; TODO Handle price object in element list, taking total_vat_excl for the summation?
  (setv total-vat-excl (compute-price prestations :count-optional count-optional))
  (if (numeric? vat-rate)
    (do
      (setv vat (if (none? total-vat-excl) None (compute-vat total-vat-excl vat-rate)))
      {
        "vat" vat
        "total_vat_incl" (if (none? total-vat-excl) None (+ total-vat-excl vat))
        "total_vat_excl" total-vat-excl
      }
    )
    {
      "vat" None
      "total_vat_incl" total-vat-excl
      "total_vat_excl" total-vat-excl
    }))

(defn parse-batch [batch]
  (if (none? batch)
    None
    (str batch)))

;; Data recomposition/derivation from previously parsed data.

(defn has-section? [prestation]
  (and (in "section" prestation) (not (none? (get prestation "section")))))

(defn not-has-section? [prestation]
  (not (has-section? prestation)))

(defn has-batch? [prestation]
  (and (in "batch" prestation) (not (none? (get prestation "batch")))))

(defn is-optional? [prestation]
  (get prestation "optional"))

(defn recompose-prestations [sections all-prestations]
  "Recompose prestations: is equal to all sections and all non-section prestations."
  (+ [] sections (list (filter not-has-section? all-prestations))))

(defn recompose-batches [all-prestations]
  "Recompose batches"
  ;; Get all batch names.
  (defn unique-batch-names [prestation]
    (reduce (fn [batches prestation]
    (setv batch (get prestation "batch"))
    (if (and (not (none? batch)) (not (in batch batches)))
      (.append batches batch))
      batches) all-prestations []))
  ;; Get all prestations that match the name.
  (defn batch-prestations [batch-name all-prestations]
    (list (filter (fn [prestation]
      (= (get prestation "batch") batch-name)) all-prestations)))
  ;; map-batch: get batch prestations and derive price.
  (defn map-batch [batch-name]
    (setv prestations (batch-prestations batch-name all-prestations))
    {
      "name" batch-name
      "prestations" prestations
      "price" (compute-price prestations)
    })
  (list (map map-batch (unique-batch-names all-prestations))))

(defn recompose-optional-prestations [sections all-prestations]
  "Recompose optional prestations: is equal to all optional sections and all optional non-section prestations."
  (+
    []
    (list (filter is-optional? sections))
    (list (filter (fn [prestation] (and (is-optional? prestation) (not-has-section? prestation))) all-prestations))
  ))

(defn get-file-extension [filename]
  (get (.splitext os.path filename) 1))

(defn parse-resource [resource]
  (if (.startswith resource "http")
    { "path" (+ "__logo" (get-file-extension resource)) "url" resource}
    { "path" resource "file" resource }))

(defn parse-logo [logo]
  (if (none? logo)
    None
    (parse-resource logo)))

(defn parse-sect [sect]
  (merge-dicts [
    (parse-dict-values sect
      ["name" "email"]
      ; TODO Allows to pass other metadata / properties.
      ["logo" "logo_tex"])
    {
      "logo" (parse-logo (get-default sect "logo" None))
    }]))

(defn parse-quote [definition]
  """
  Parse and normalize a quote definition.
  """
  (setv (, all-prestations sections)
    (parse-all-prestations (get definition "prestations")))
  (setv (, all-optional-prestations optional-sections)
    (parse-all-prestations (recompose-optional-prestations sections all-prestations)))
  (setv vat-rate (get-default definition "vat_rate" None))
  (setv has-quantities (any (map (fn [prestation] (> (get prestation "quantity") 1)) all-prestations)))
  (merge-dicts [
    ;; TODO Make the validation of the input dict recursive.
    (parse-dict-values definition
      ["title" "date" "author" "place" "sect" "client" "legal" "object" "prestations"]
      ["context" "version" "definitions" "conditions" "documents" "display_project_reference" "vat_rate"])
    {
      "sect" (parse-sect (get definition "sect"))
      "vat_rate" vat_rate
      "price" (compute-price-vat all-prestations :vat-rate vat-rate)
      ;; Derive sections from all-prestations (and sections too).
      "batches" (recompose-batches all-prestations)
      "all_prestations" all-prestations
      "sections" sections
      ;; Derive from section and all_prestations.
      "has_quantities" has-quantities
      "prestations" (recompose-prestations sections all-prestations)
      "optional_prestations" all-optional-prestations
      "optional_sections" optional-sections
      "optional_price" (compute-price-vat all-optional-prestations :count-optional True :vat-rate vat-rate)
      "display_project_reference" (none-or-true? (get-default definition "display_project_reference" True))
    }]))

(defn parse-line [line]
  (merge-dicts [
    (parse-dict-values line
      ["title" "price"]
      ["description" "quantity"])
    {
      "quantity" (get-default line "quantity" 1)
      "total" (compute-price [line] :count-optional True)
    }
  ]))

(defn parse-invoice [invoice invoices]
  (setv lines (list (map parse-line (get invoice "lines"))))
  (setv has-quantities (any (map (fn [line] (> (get line "quantity") 1)) lines)))
  (setv common-values (pick-by (fn [key]
    (in key ["author" "sect" "client" "legal" "vat_rate" "display_project_reference"])) invoices))
  (setv merged-invoice (merge-dicts [
    ;; Insert common values.
    common-values
    ;; Override by invoice ones if present (not None).
    (filter-dict
      (parse-dict-values invoice
        ["number" "date" "lines"]
        ["author" "sect" "client" "legal" "closing_note" "title" "vat_rate" "display_project_reference"])
      (fn [value key]
        (or (not (none? value)) (not (in key common-values)))))
    ]))
  (merge-dicts [
    merged-invoice
    {
      "sect" (parse-sect (get merged-invoice "sect"))
      "lines" lines
      "has_quantities" has-quantities
      "vat_rate" (get merged-invoice "vat_rate")
      "price" (compute-price-vat lines :vat-rate (get merged-invoice "vat_rate"))
      "display_project_reference" (none-or-true? (get-default merged-invoice "display_project_reference" True))
    }]))

(defn parse-invoices [definition]
  """
  Parse and normalize invoices definition.
  """
  (defn parse-invoice-closure [invoice]
    (parse-invoice invoice definition))
  (parse-dict-values definition
    ["author" "sect" "client" "legal" "invoices"]
    [])
  {
    "invoices" (list (map parse-invoice-closure (get definition "invoices")))
  })
