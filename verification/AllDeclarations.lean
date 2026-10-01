import KarpPurbhoo
import Lean.Util.CollectAxioms

set_option maxHeartbeats 0 in
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let allowed : Array Name := #[``Classical.choice, ``propext, ``Quot.sound]
  let mut count : Nat := 0
  let mut proofs : Nat := 0
  let mut pending : Array Name := #[]
  for idx in [:env.header.moduleNames.size] do
    let modName := env.header.moduleNames[idx]!
    unless (`FewInflection).isPrefixOf modName || (`ModifiedCartan).isPrefixOf modName || (`KarpPurbhoo).isPrefixOf modName do
      continue
    let modData := env.header.moduleData[idx]!
    for idx in [:modData.constNames.size] do
      count := count + 1
      if modData.constants[idx]!.isTheorem then proofs := proofs + 1
      pending := pending.push modData.constNames[idx]!
  if proofs == 0 then throwError "No project proofs were audited"
  -- Same dependency edges as Lean.Util.CollectAxioms, shared across all roots.
  let mut seen : NameSet := {}
  let mut used : NameSet := {}
  while !pending.isEmpty do
    let name := pending.back!
    pending := pending.pop
    if seen.contains name then continue
    seen := seen.insert name
    let some info := env.checked.get.find? name
      | throwError "Missing kernel declaration: {name}"
    pending := pending ++ info.type.getUsedConstants
    match info with
    | .axiomInfo _ =>
      unless allowed.contains name do
        throwError "Forbidden logical dependency: {name}"
      used := used.insert name
    | .defnInfo v => pending := pending ++ v.value.getUsedConstants
    | .thmInfo v => pending := pending ++ v.value.getUsedConstants
    | .opaqueInfo v => pending := pending ++ v.value.getUsedConstants
    | .inductInfo v => pending := pending ++ v.ctors.toArray
    | _ => pure ()
  logInfo m!"AUDIT PASSED: {count} declarations, including {proofs} theorem declarations."
  logInfo m!"Actual logical dependencies: {used.toArray}."

